@file:Suppress("UNUSED_PARAMETER", "OPT_IN_USAGE")

package com.kineticguard.app

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageFormat
import android.graphics.Matrix
import android.graphics.Rect
import android.graphics.YuvImage
import android.os.Bundle
import android.util.Log
import android.widget.FrameLayout
import androidx.activity.ComponentActivity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.content.ContextCompat
import com.google.mediapipe.framework.image.BitmapImageBuilder
import com.google.mediapipe.tasks.core.BaseOptions
import com.google.mediapipe.tasks.vision.core.RunningMode
import com.google.mediapipe.tasks.vision.handlandmarker.HandLandmarker
import com.kineticguard.data.local.TokenManager
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.io.ByteArrayOutputStream
import java.nio.ByteBuffer
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import kotlin.math.hypot

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            KineticGuardApp()
        }
    }
}

@Composable
fun KineticGuardApp() {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var hasPermission by remember { mutableStateOf(false) }
    var statusText by remember { mutableStateOf("Requesting Camera...") }
    var brain: OnnxModel? by remember { mutableStateOf(null) }
    var landmarker: HandLandmarker? by remember { mutableStateOf(null) }

    val permissionLauncher = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        hasPermission = permissions[Manifest.permission.CAMERA] == true
        if (!hasPermission) statusText = "Camera permission denied!"
    }

    LaunchedEffect(Unit) {
        permissionLauncher.launch(arrayOf(
            Manifest.permission.CAMERA,
            Manifest.permission.ACCESS_FINE_LOCATION
        ))

        val manager = TokenManager(context)
        val token = manager.getToken()

        if (token.isNullOrEmpty()) {
            scope.launch(Dispatchers.IO) {
                try {
                    val loginRes = ApiClient.instance.login(
                        LoginRequest("test@kineticguard.com", "mypassword123")
                    )
                    manager.saveToken(loginRes.accessToken)
                    currentToken = loginRes.accessToken
                    Log.d("AUTH", "Successfully logged in! Token saved.")
                } catch (e: Exception) {
                    Log.e("AUTH", "Login failed ERROR: ${e.message}")
                }
            }
        } else {
            currentToken = token
        }

        try {
            brain = OnnxModel(context)
            val baseOpts = BaseOptions.builder()
                .setModelAssetPath("hand_landmarker.task")
                .build()
            val opts = HandLandmarker.HandLandmarkerOptions.builder()
                .setBaseOptions(baseOpts)
                .setRunningMode(RunningMode.VIDEO)
                .setNumHands(1)
                .build()
            landmarker = HandLandmarker.createFromOptions(context, opts)
            statusText = "Ready. Show specific fingers!"
        } catch (e: Exception) {
            statusText = "Error loading model: ${e.message}"
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        if (hasPermission) {
            Box(modifier = Modifier.weight(1f)) {
                AndroidView(
                    factory = { ctx ->
                        FrameLayout(ctx).also { frame ->
                            val preview = PreviewView(ctx)
                            frame.addView(preview)

                            val overlay = HandOverlayView(ctx)
                            frame.addView(overlay)

                            startCamera(ctx, preview) { imageProxy ->
                                val currentBrain = brain
                                val currentEyes = landmarker
                                if (currentBrain != null && currentEyes != null) {
                                    processFrame(imageProxy, currentEyes, currentBrain, overlay) { detectedGesture ->
                                        if (detectedGesture != "NONE") {
                                            statusText = "Detected: $detectedGesture! Sending..."
                                            sendSosAlert(context, detectedGesture)
                                        }
                                    }
                                }
                            }
                        }
                    }
                )

                // NEW: Stealth gradient overlay at the top
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(100.dp)
                        .background(
                            brush = Brush.verticalGradient(
                                colors = listOf(Color.Black.copy(alpha = 0.8f), Color.Transparent)
                            )
                        )
                ) {
                    Text(
                        text = "KINETIC GUARD",
                        color = Color.White.copy(alpha = 0.7f),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(16.dp)
                    )
                }
            }
        } else {
            Box(modifier = Modifier.weight(1f), contentAlignment = Alignment.Center) {
                Text("Waiting for Camera...", color = Color.White, fontSize = 24.sp)
            }
        }

        // NEW: Premium Status Bar at the bottom
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    color = if (statusText.contains("Sending")) Color(0xFFFFA500) else Color(0xFFB71C1C), // Orange if sending, Red if ready
                    shape = RoundedCornerShape(topStart = 16.dp, topEnd = 16.dp)
                )
                .padding(24.dp),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = statusText,
                color = Color.White,
                fontSize = 20.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

private var cameraExecutor: ExecutorService? = null
private var lastAlertTime = 0L
private var lastDetectedGesture: String = "NONE"
private var currentToken: String? = null

private fun startCamera(
    context: Context,
    previewView: PreviewView,
    onFrame: (ImageProxy) -> Unit
) {
    cameraExecutor = Executors.newSingleThreadExecutor()
    val cameraProviderFuture = ProcessCameraProvider.getInstance(context)

    cameraProviderFuture.addListener({
        val cameraProvider = cameraProviderFuture.get()
        val preview = Preview.Builder().build().also {
            it.setSurfaceProvider(previewView.surfaceProvider)
        }

        val imageAnalyzer = ImageAnalysis.Builder()
            .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
            .build()
            .also {
                it.setAnalyzer(cameraExecutor!!, onFrame)
            }

        val cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA

        try {
            cameraProvider.unbindAll()
            cameraProvider.bindToLifecycle(
                (context as ComponentActivity), cameraSelector, preview, imageAnalyzer
            )
        } catch (e: Exception) {
            Log.e("Camera", "Failed", e)
        }
    }, ContextCompat.getMainExecutor(context))
}

@Suppress("OPT_IN_USAGE")
private fun processFrame(
    imageProxy: ImageProxy,
    landmarker: HandLandmarker,
    brain: OnnxModel,
    overlay: HandOverlayView,
    onGestureDetected: (String) -> Unit
) {
    val bitmap = imageProxy.toBitmapCompat()
    val rotation = imageProxy.imageInfo.rotationDegrees
    val matrix = Matrix()
    matrix.postRotate(rotation.toFloat())
    val rotatedBitmap = Bitmap.createBitmap(bitmap, 0, 0, bitmap.width, bitmap.height, matrix, true)
    val mpImage = BitmapImageBuilder(rotatedBitmap).build()
    val result = landmarker.detectForVideo(mpImage, System.currentTimeMillis())

    if (result.landmarks().isNotEmpty()) {
        val hand = result.landmarks()[0]
        val points = hand.map { it.x() to it.y() }
        overlay.landmarks = points

        val detectedGesture = getFingerTriggerString(hand)

        val now = System.currentTimeMillis()
        // STRICT 3-second cooldown to prevent spam
        if (detectedGesture != "NONE" && now - lastAlertTime > 3000) {
            lastAlertTime = now
            lastDetectedGesture = detectedGesture
            onGestureDetected(detectedGesture)
        }
    } else {
        overlay.landmarks = null
        lastDetectedGesture = "NONE"
    }
    imageProxy.close()
}

private fun dist(a: com.google.mediapipe.tasks.components.containers.NormalizedLandmark,
                 b: com.google.mediapipe.tasks.components.containers.NormalizedLandmark): Float {
    return hypot((a.x() - b.x()).toDouble(), (a.y() - b.y()).toDouble()).toFloat()
}

private fun getFingerTriggerString(hand: List<com.google.mediapipe.tasks.components.containers.NormalizedLandmark>): String {
    // STRICT margin to ignore natural finger micro-movements
    val indexUp = hand[8].y() < hand[6].y() - 0.10f
    val middleUp = hand[12].y() < hand[10].y() - 0.10f
    val ringUp = hand[16].y() < hand[14].y() - 0.10f
    val pinkyUp = hand[20].y() < hand[18].y() - 0.10f

    val thumbTip = hand[4]
    val thumbIp = hand[3]
    val thumbMcp = hand[2]
    val wrist = hand[0]
    val indexMcp = hand[5]

    val thumbYUp = thumbTip.y() < thumbIp.y() - 0.10f
    val thumbExtended = dist(thumbTip, wrist) > dist(thumbMcp, wrist) * 1.2f
    val thumbTucked = dist(thumbTip, indexMcp) < 0.12f
    val thumbUp = thumbYUp && thumbExtended && !thumbTucked

    val thumbDown = (thumbTip.y() > thumbIp.y() + 0.10f) || thumbTucked

    val fingerCount = listOf(indexUp, middleUp, ringUp, pinkyUp).count { it }
    val totalCount = fingerCount + if (thumbUp) 1 else 0

    return when {
        totalCount == 5 -> "ALL_FIVE_UP"
        fingerCount == 4 && !thumbUp -> "FOUR_FINGERS_UP"
        totalCount == 3 -> when {
            indexUp && middleUp && ringUp -> "INDEX_MIDDLE_RING_UP"
            indexUp && middleUp && pinkyUp -> "INDEX_MIDDLE_PINKY_UP"
            indexUp && ringUp && pinkyUp -> "INDEX_RING_PINKY_UP"
            middleUp && ringUp && pinkyUp -> "MIDDLE_RING_PINKY_UP"
            else -> "THREE_FINGERS_UP"
        }
        totalCount == 2 -> when {
            indexUp && middleUp -> "INDEX_MIDDLE_UP"
            indexUp && ringUp -> "INDEX_RING_UP"
            middleUp && ringUp -> "MIDDLE_RING_UP"
            middleUp && pinkyUp -> "MIDDLE_PINKY_UP"
            ringUp && pinkyUp -> "RING_PINKY_UP"
            thumbUp && indexUp -> "THUMB_INDEX_UP"
            thumbUp && pinkyUp -> "THUMB_PINKY_UP"
            else -> "TWO_FINGERS_UP"
        }
        totalCount == 1 -> when {
            indexUp -> "INDEX_UP"
            middleUp -> "MIDDLE_UP"
            ringUp -> "RING_UP"
            pinkyUp -> "PINKY_UP"
            thumbUp -> "THUMB_UP"
            else -> "ONE_FINGER_UP"
        }
        thumbDown && fingerCount == 0 -> "THUMB_DOWN"
        else -> "NONE"
    }
}

@Suppress("unused")
private fun extract210Features(hand: List<com.google.mediapipe.tasks.components.containers.NormalizedLandmark>): FloatArray {
    val features = mutableListOf<Float>()
    for (i in 0 until 20) {
        for (j in (i + 1) until 21) {
            val dx = hand[i].x() - hand[j].x()
            val dy = hand[i].y() - hand[j].y()
            features.add(hypot(dx, dy).toFloat())
        }
    }
    return features.toFloatArray()
}

private fun sendSosAlert(context: Context, gestureString: String) {
    val token = currentToken

    if (token.isNullOrEmpty()) {
        Log.e("SOS", "Cannot send SOS: No authentication token!")
        return
    }

    if (ContextCompat.checkSelfPermission(context, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                ApiClient.instance.sendSos("Bearer $token", SosRequest(
                    triggerMethod = gestureString,
                    latitude = 0.0,
                    longitude = 0.0
                ))
            } catch (e: Exception) {
                Log.e("SOS", "Failed: ${e.message}")
            }
        }
        return
    }

    val fusedLocationClient = com.google.android.gms.location.LocationServices.getFusedLocationProviderClient(context)

    try {
        fusedLocationClient.lastLocation.addOnSuccessListener { location ->
            val lat = location?.latitude ?: 0.0
            val lon = location?.longitude ?: 0.0

            CoroutineScope(Dispatchers.IO).launch {
                try {
                    ApiClient.instance.sendSos("Bearer $token", SosRequest(
                        triggerMethod = gestureString,
                        latitude = lat,
                        longitude = lon
                    ))
                    Log.d("SOS", "Sent $gestureString with location: $lat, $lon")
                } catch (e: Exception) {
                    Log.e("SOS", "Failed: ${e.message}")
                }
            }
        }
    } catch (e: SecurityException) {
        Log.e("SOS", "Location permission denied: ${e.message}")
    }
}

@Suppress("OPT_IN_USAGE")
private fun ImageProxy.toBitmapCompat(): Bitmap {
    val image = this.image ?: throw IllegalStateException("ImageProxy has no image")
    val planes = image.planes
    val yBuffer: ByteBuffer = planes[0].buffer
    val uBuffer: ByteBuffer = planes[1].buffer
    val vBuffer: ByteBuffer = planes[2].buffer

    val ySize = yBuffer.remaining()
    val uSize = uBuffer.remaining()
    val vSize = vBuffer.remaining()

    val nv21 = ByteArray(ySize + uSize + vSize)
    yBuffer.get(nv21, 0, ySize)
    vBuffer.get(nv21, ySize, vSize)
    uBuffer.get(nv21, ySize + vSize, uSize)

    val yuvImage = YuvImage(nv21, ImageFormat.NV21, this.width, this.height, null)
    val out = ByteArrayOutputStream()
    yuvImage.compressToJpeg(Rect(0, 0, this.width, this.height), 100, out)
    val jpegBytes = out.toByteArray()
    return BitmapFactory.decodeByteArray(jpegBytes, 0, jpegBytes.size)
        ?: throw IllegalStateException("Failed to decode JPEG from ImageProxy")
}