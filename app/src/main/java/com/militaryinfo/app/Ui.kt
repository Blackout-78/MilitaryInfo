package com.militaryinfo.app

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.Color
import android.graphics.Typeface
import android.graphics.drawable.GradientDrawable
import android.util.TypedValue
import android.view.Gravity
import android.view.View
import android.view.ViewGroup
import android.widget.HorizontalScrollView
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.TextView

object Night {
    val navy: Int = Color.parseColor("#0B1426")
    val charcoal: Int = Color.parseColor("#1A1F2B")
    val raised: Int = Color.parseColor("#242A38")
    val border: Int = Color.parseColor("#33405A")
    val text: Int = Color.WHITE
    val muted: Int = Color.parseColor("#B8C2D6")
    val accent: Int = Color.parseColor("#6FA8FF")
}

const val MATCH = ViewGroup.LayoutParams.MATCH_PARENT
const val WRAP = ViewGroup.LayoutParams.WRAP_CONTENT

fun Context.dp(v: Int): Int = (v * resources.displayMetrics.density + 0.5f).toInt()

fun Context.box(fill: Int, stroke: Int? = null, radiusDp: Int = 12): GradientDrawable =
    GradientDrawable().apply {
        setColor(fill)
        cornerRadius = dp(radiusDp).toFloat()
        if (stroke != null) setStroke(1, stroke)
    }

fun lp(w: Int = MATCH, h: Int = WRAP, weight: Float = 0f): LinearLayout.LayoutParams =
    LinearLayout.LayoutParams(w, h, weight)

fun LinearLayout.LayoutParams.margins(l: Int = 0, t: Int = 0, r: Int = 0, b: Int = 0): LinearLayout.LayoutParams {
    setMargins(l, t, r, b)
    return this
}

fun Context.label(
    text: CharSequence,
    sizeSp: Float = 14f,
    color: Int = Night.text,
    medium: Boolean = false
): TextView = TextView(this).apply {
    this.text = text
    setTextSize(TypedValue.COMPLEX_UNIT_SP, sizeSp)
    setTextColor(color)
    if (medium) typeface = Typeface.create("sans-serif-medium", Typeface.NORMAL)
    setLineSpacing(0f, 1.15f)
}

fun Context.chip(text: String, selected: Boolean): TextView = label(text, 12f).apply {
    setPadding(dp(12), dp(6), dp(12), dp(6))
    gravity = Gravity.CENTER
    styleChip(this, selected)
}

fun Context.styleChip(chip: TextView, selected: Boolean) {
    if (selected) {
        chip.background = box(Night.accent, null, 20)
        chip.setTextColor(Night.navy)
        chip.typeface = Typeface.create("sans-serif-medium", Typeface.NORMAL)
    } else {
        chip.background = box(Night.charcoal, Night.border, 20)
        chip.setTextColor(Night.text)
        chip.typeface = Typeface.DEFAULT
    }
}

class ChipRow(
    private val context: Context,
    options: List<Pair<String?, String>>,
    private val onPick: (String?) -> Unit
) {
    private val chips = ArrayList<Pair<String?, TextView>>()
    private var selected: String? = null
    val view: HorizontalScrollView = HorizontalScrollView(context).apply {
        isHorizontalScrollBarEnabled = false
        overScrollMode = View.OVER_SCROLL_NEVER
    }

    init {
        val row = LinearLayout(context).apply { orientation = LinearLayout.HORIZONTAL }
        options.forEachIndexed { i, (key, text) ->
            val c = context.chip(text, i == 0)
            c.setOnClickListener { pick(key) }
            row.addView(c, lp(WRAP, WRAP).margins(r = context.dp(6)))
            chips.add(key to c)
        }
        view.addView(row)
    }

    private fun pick(key: String?) {
        selected = key
        chips.forEach { (k, c) -> context.styleChip(c, k == key) }
        onPick(key)
    }
}

fun Context.proofChip(proof: Proof): TextView {
    val (fill, ink) = when (proof) {
        Proof.OFFICIAL -> Color.parseColor("#123524") to Color.parseColor("#7BE0A4")
        Proof.HISTORICAL -> Color.parseColor("#14305A") to Color.parseColor("#8FBFFF")
        Proof.UNVERIFIED -> Color.parseColor("#3D2E0A") to Color.parseColor("#F2C46B")
    }
    return label(proof.label, 11f, ink, medium = true).apply {
        setPadding(dp(8), dp(3), dp(8), dp(3))
        background = box(fill, null, 6)
    }
}

fun Context.pill(text: String): TextView = label(text, 11f, Night.muted).apply {
    setPadding(dp(8), dp(3), dp(8), dp(3))
    background = box(Night.raised, Night.border, 6)
}

fun Context.swatchLine(s: Swatch): LinearLayout {
    val row = LinearLayout(this).apply {
        orientation = LinearLayout.HORIZONTAL
        gravity = Gravity.CENTER_VERTICAL
    }
    val color = try {
        Color.parseColor(s.hex)
    } catch (e: IllegalArgumentException) {
        Night.muted
    }
    val dot = View(this).apply { background = box(color, Night.border, 4) }
    row.addView(dot, lp(dp(16), dp(16)).margins(r = dp(8)))
    row.addView(label("${s.role}: ${s.name}", 12f, Night.muted))
    return row
}

fun Context.loadAssetImage(name: String?): Bitmap? {
    if (name == null) return null
    return try {
        assets.open("images/$name").use { BitmapFactory.decodeStream(it) }
    } catch (e: java.io.IOException) {
        null
    }
}

fun Context.imageBox(name: String?, heightDp: Int, widthDp: Int? = null): View {
    val bmp = loadAssetImage(name)
    val w = if (widthDp != null) dp(widthDp) else MATCH
    return if (bmp != null) {
        ImageView(this).apply {
            setImageBitmap(bmp)
            scaleType = ImageView.ScaleType.FIT_CENTER
            background = box(Night.raised, Night.border, 8)
            layoutParams = lp(w, dp(heightDp))
        }
    } else {
        label("Image to add", 11f, Night.muted).apply {
            gravity = Gravity.CENTER
            background = box(Night.raised, Night.border, 8)
            layoutParams = lp(w, dp(heightDp))
        }
    }
}
