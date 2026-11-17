package com.militaryinfo.app

import android.content.Context
import android.view.Gravity
import android.view.View
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ScrollView

class DetailView(
    context: Context,
    private val entry: Entry,
    private val allEntries: List<Entry>,
    private val onOpen: (Entry) -> Unit,
    onBack: () -> Unit
) : LinearLayout(context) {

    init {
        orientation = VERTICAL

        val back = LinearLayout(context).apply {
            orientation = HORIZONTAL
            gravity = Gravity.CENTER_VERTICAL
            setPadding(context.dp(12), context.dp(10), context.dp(16), context.dp(10))
            setOnClickListener { onBack() }
        }
        val arrow = ImageView(context).apply {
            setImageResource(R.drawable.ic_chevron_left)
            setColorFilter(Night.accent)
        }
        back.addView(arrow, lp(context.dp(24), context.dp(24)))
        back.addView(context.label("Back", 14f, Night.accent, medium = true))
        addView(back, lp(WRAP, WRAP))

        val body = LinearLayout(context).apply {
            orientation = VERTICAL
            setPadding(context.dp(16), 0, context.dp(16), context.dp(40))
        }
        build(body)
        val scroll = ScrollView(context).apply { isVerticalScrollBarEnabled = false }
        scroll.addView(body, lp())
        addView(scroll, lp(MATCH, 0, 1f))
    }

    private fun build(body: LinearLayout) {
        val c = context
        body.addView(c.imageBox(entry.image, 180), lp())
        body.addView(c.label(entry.name, 22f, medium = true), lp().margins(t = c.dp(14)))

        val tags = LinearLayout(c).apply { orientation = HORIZONTAL }
        tags.addView(c.proofChip(entry.proof), lp(WRAP, WRAP).margins(r = c.dp(6)))
        tags.addView(c.pill(entry.group), lp(WRAP, WRAP).margins(r = c.dp(6)))
        entry.years()?.let { tags.addView(c.pill(it), lp(WRAP, WRAP)) }
        body.addView(tags, lp().margins(t = c.dp(8)))

        val branchText = entry.branches.joinToString(", ") { Branches.short(it) }
        body.addView(c.label("Branches: $branchText", 12f, Night.muted), lp().margins(t = c.dp(8)))
        val eraText = entry.eras.joinToString(", ") { Eras.label(it) }
        body.addView(c.label("Eras: $eraText", 12f, Night.muted), lp().margins(t = c.dp(2)))

        body.addView(c.label(entry.summary, 15f), lp().margins(t = c.dp(14)))

        entry.remember?.let { hook ->
            val card = LinearLayout(c).apply {
                orientation = VERTICAL
                background = c.box(Night.raised, Night.accent, 10)
                setPadding(c.dp(14), c.dp(10), c.dp(14), c.dp(10))
            }
            card.addView(c.label("Remember it", 12f, Night.accent, medium = true))
            card.addView(c.label(hook, 14f), lp().margins(t = c.dp(2)))
            body.addView(card, lp().margins(t = c.dp(14)))
        }

        if (entry.facts.isNotEmpty()) {
            heading(body, "Key facts")
            entry.facts.forEach { f ->
                body.addView(c.label("•  $f", 14f), lp().margins(t = c.dp(4)))
            }
        }

        if (entry.swatches.isNotEmpty()) {
            heading(body, "Colors")
            entry.swatches.forEach { body.addView(c.swatchLine(it), lp().margins(t = c.dp(4))) }
        }

        if (entry.variants.isNotEmpty()) {
            heading(body, "Variations")
            entry.variants.forEach { body.addView(variantCard(it), lp().margins(t = c.dp(8))) }
        }

        entry.attachments.forEach { a ->
            heading(body, if (entry.tab == Tab.BADGES.key) "Hangs underneath: ${a.name}" else "Worn with: ${a.name}")
            val target = a.link?.let { id -> allEntries.firstOrNull { it.id == id } }
            if (target != null) {
                val open = c.label("Open ${target.name}  \u203A", 14f, Night.accent, medium = true)
                open.setPadding(0, c.dp(8), 0, c.dp(8))
                open.setOnClickListener { onOpen(target) }
                body.addView(open, lp().margins(t = c.dp(4)))
            }
            a.note?.let { body.addView(c.label(it, 13f, Night.muted), lp().margins(t = c.dp(4))) }
            a.variants.forEach { body.addView(variantCard(it), lp().margins(t = c.dp(8))) }
        }

        heading(body, "Source")
        if (entry.sources.isEmpty()) {
            body.addView(
                c.label("No source yet. This entry stays unverified until one is added.", 13f, Night.muted),
                lp().margins(t = c.dp(4))
            )
        } else {
            entry.sources.forEach { body.addView(c.label("•  $it", 13f, Night.muted), lp().margins(t = c.dp(4))) }
        }
    }

    private fun heading(body: LinearLayout, text: String) {
        body.addView(context.label(text, 13f, Night.accent, medium = true), lp().margins(t = context.dp(20)))
    }

    private fun variantEntry(v: Variant): Entry {
        val meta = listOfNotNull(finishLabel(v.finish), genderLabel(v.gender), v.uniform, v.era?.let { Eras.label(it) })
        return entry.copy(
            id = entry.id + ":" + v.label,
            name = v.label,
            group = entry.name,
            eras = v.era?.let { listOf(it) } ?: entry.eras,
            summary = v.note ?: entry.summary,
            facts = meta,
            remember = null,
            swatches = v.swatches,
            variants = emptyList(),
            attachments = emptyList(),
            image = v.image ?: (if (entry.variants.any { it.image != null }) null else entry.image)
        )
    }

    private fun variantCard(v: Variant): View {
        val c = context
        val card = LinearLayout(c).apply {
            orientation = HORIZONTAL
            background = c.box(Night.charcoal, Night.border, 12)
            setPadding(c.dp(12), c.dp(10), c.dp(12), c.dp(10))
        }
        if (v.image != null) {
            card.addView(c.imageBox(v.image, 56, 56), lp(c.dp(56), c.dp(56)).margins(r = c.dp(12)))
        }
        val col = LinearLayout(c).apply { orientation = VERTICAL }
        col.addView(c.label(v.label, 14f, medium = true))
        val meta = listOfNotNull(
            finishLabel(v.finish),
            genderLabel(v.gender),
            v.uniform,
            v.era?.let { Eras.label(it) }
        ).joinToString(" · ")
        if (meta.isNotEmpty()) col.addView(c.label(meta, 12f, Night.muted), lp().margins(t = c.dp(2)))
        v.note?.let { col.addView(c.label(it, 13f), lp().margins(t = c.dp(4))) }
        v.swatches.forEach { col.addView(c.swatchLine(it), lp().margins(t = c.dp(4))) }
        card.addView(col, lp(0, WRAP, 1f))
        card.addView(c.label("\u203A", 22f, Night.accent), lp(WRAP, WRAP).apply { gravity = Gravity.CENTER_VERTICAL })
        card.setOnClickListener { onOpen(variantEntry(v)) }
        return card
    }

    private fun finishLabel(finish: String?): String? = when (finish) {
        null -> null
        "polished" -> "Polished (shiny)"
        "subdued" -> "Subdued (non-shiny)"
        else -> finish.replaceFirstChar { it.uppercase() }
    }

    private fun genderLabel(gender: String?): String? = when (gender) {
        null -> null
        "any" -> "Male and female"
        else -> gender.replaceFirstChar { it.uppercase() }
    }
}
