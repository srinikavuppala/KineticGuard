package com.kineticguard.app

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.Path
import android.util.AttributeSet
import android.view.View

class HandOverlayView @JvmOverloads constructor(
    context: Context, attrs: AttributeSet? = null
) : View(context, attrs) {

    private val dotPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.YELLOW
        style = Paint.Style.FILL
        strokeWidth = 4f
    }

    private val linePaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        color = Color.YELLOW
        style = Paint.Style.STROKE
        strokeWidth = 3f
        isAntiAlias = true
    }

    // Hand skeleton connections
    private val connections = listOf(
        // Thumb
        0 to 1, 1 to 2, 2 to 3, 3 to 4,
        // Index
        0 to 5, 5 to 6, 6 to 7, 7 to 8,
        // Middle
        0 to 9, 9 to 10, 10 to 11, 11 to 12,
        // Ring
        0 to 13, 13 to 14, 14 to 15, 15 to 16,
        // Pinky
        0 to 17, 17 to 18, 18 to 19, 19 to 20,
        // Palm base
        5 to 9, 9 to 13, 13 to 17
    )

    var landmarks: List<Pair<Float, Float>>? = null
        set(value) {
            field = value
            postInvalidate()
        }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val points = landmarks ?: return

        // Mirror X to match front camera preview
        val mirrored = points.map { (1f - it.first) to it.second }

        // Draw connections
        for ((start, end) in connections) {
            if (start < mirrored.size && end < mirrored.size) {
                val path = Path()
                path.moveTo(mirrored[start].first * width, mirrored[start].second * height)
                path.lineTo(mirrored[end].first * width, mirrored[end].second * height)
                canvas.drawPath(path, linePaint)
            }
        }

        // Draw dots
        for ((x, y) in mirrored) {
            canvas.drawCircle(x * width, y * height, 8f, dotPaint)
        }
    }
}