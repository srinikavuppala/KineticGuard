package com.kineticguard.app

import android.content.Context
import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import java.io.File
import java.io.FileOutputStream
import java.nio.FloatBuffer

class OnnxModel(context: Context) {
    private val env = OrtEnvironment.getEnvironment()
    private val session: OrtSession

    init {
        val assetFile = context.assets.open("gesture_model.onnx")
        val tempFile = File(context.cacheDir, "gesture_model.onnx")
        FileOutputStream(tempFile).use { out -> assetFile.copyTo(out) }

        val options = OrtSession.SessionOptions()
        session = env.createSession(tempFile.absolutePath, options)
    }

    fun predict(features: FloatArray): String {
        val shape = longArrayOf(1, 210)
        val buffer = FloatBuffer.wrap(features)
        val tensor = OnnxTensor.createTensor(env, buffer, shape)

        val inputName = session.inputNames.iterator().next()
        val results = session.run(mapOf(inputName to tensor))

        // FIXED: Handle both int64 (argmax) and float32 (probabilities) outputs
        val rawOutput = results[0].value
        val classIndex = when (rawOutput) {
            is LongArray -> rawOutput[0].toInt()
            is Array<*> -> {
                val probs = rawOutput[0] as FloatArray
                probs.indices.maxByOrNull { probs[it] } ?: -1
            }
            else -> -1
        }

        tensor.close()
        results.close()

        return if (classIndex == 1) "GESTURE" else "IGNORE"
    }
}