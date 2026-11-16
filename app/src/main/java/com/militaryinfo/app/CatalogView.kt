package com.militaryinfo.app

import android.content.Context
import android.graphics.Color
import android.graphics.drawable.ColorDrawable
import android.text.Editable
import android.text.TextWatcher
import android.util.TypedValue
import android.view.View
import android.view.ViewGroup
import android.view.inputmethod.EditorInfo
import android.widget.BaseAdapter
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.ListView

class CatalogView(
    context: Context,
    private val tab: Tab,
    entries: List<Entry>,
    emptyMessage: String,
    private val onOpen: (Entry) -> Unit
) : LinearLayout(context) {

    private val all: List<Entry> = entries.filter { it.tab == tab.key }
    private var shown: List<Entry> = all
    private var query: String = ""
    private var branch: String? = null
    private var era: String? = null
    private var group: String? = null
    private var gender: String? = null

    private val list = ListView(context)
    private val empty = context.label(emptyMessage, 14f, Night.muted)

    private val adapter = object : BaseAdapter() {
        override fun getCount(): Int = shown.size
        override fun getItem(position: Int): Any = shown[position]
        override fun getItemId(position: Int): Long = position.toLong()
        override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
            val row = (convertView as? EntryRow) ?: EntryRow(parent.context)
            row.bind(shown[position])
            return row
        }
    }

    init {
        orientation = VERTICAL
        val side = context.dp(16)

        addView(context.label(tab.title, 22f, medium = true), lp().margins(side, context.dp(8), side, context.dp(10)))
        addView(searchField(), lp().margins(side, 0, side, context.dp(10)))

        val branchOptions = listOf<Pair<String?, String>>(null to "All") +
            Branches.all.map { it to Branches.short(it) }
        addView(
            ChipRow(context, branchOptions) { branch = it; refresh() }.view,
            lp().margins(side, 0, 0, context.dp(8))
        )

        val eraOptions = listOf<Pair<String?, String>>(null to "Any era") +
            Eras.all.map { it.first to it.second }
        addView(
            ChipRow(context, eraOptions) { era = it; refresh() }.view,
            lp().margins(side, 0, 0, context.dp(8))
        )

        val groups = all.map { it.group }.distinct()
        if (groups.size > 1) {
            val groupOptions = listOf<Pair<String?, String>>(null to "All types") + groups.map { it to it }
            addView(
                ChipRow(context, groupOptions) { group = it; refresh() }.view,
                lp().margins(side, 0, 0, context.dp(8))
            )
        }

        if (tab == Tab.RANKS) {
            val genderOptions = listOf<Pair<String?, String>>(
                null to "Male and female", "male" to "Male", "female" to "Female"
            )
            addView(
                ChipRow(context, genderOptions) { gender = it; refresh() }.view,
                lp().margins(side, 0, 0, context.dp(8))
            )
        }

        list.apply {
            divider = null
            dividerHeight = 0
            selector = ColorDrawable(Color.TRANSPARENT)
            clipToPadding = false
            setPadding(0, context.dp(4), 0, context.dp(32))
            overScrollMode = View.OVER_SCROLL_NEVER
            adapter = this@CatalogView.adapter
            setOnItemClickListener { _, _, position, _ -> onOpen(shown[position]) }
        }
        addView(list, lp(MATCH, 0, 1f))
        addView(empty, lp().margins(side, context.dp(16), side, 0))
        list.emptyView = empty
        refresh()
    }

    private fun searchField(): EditText = EditText(context).apply {
        hint = tab.searchHint
        setHintTextColor(Night.muted)
        setTextColor(Night.text)
        setTextSize(TypedValue.COMPLEX_UNIT_SP, 14f)
        setSingleLine(true)
        imeOptions = EditorInfo.IME_ACTION_SEARCH
        minHeight = context.dp(44)
        setPadding(context.dp(14), context.dp(8), context.dp(14), context.dp(8))
        background = context.box(Night.charcoal, Night.border, 10)
        addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                query = s?.toString().orEmpty()
                refresh()
            }
        })
    }

    private fun refresh() {
        val tokens = query.lowercase().split(' ', '\t').filter { it.isNotBlank() }
        shown = all.filter { e ->
            (branch == null || e.branches.contains(branch)) &&
                (era == null || e.eras.isEmpty() || e.eras.contains(era)) &&
                (group == null || e.group == group) &&
                e.matchesGender(gender) &&
                e.matches(tokens)
        }
        adapter.notifyDataSetChanged()
    }

    private class EntryRow(context: Context) : LinearLayout(context) {
        private val title = context.label("", 15f, medium = true)
        private val tag = context.label("", 11f, Night.accent, medium = true)
        private val summary = context.label("", 13f)
        private val meta = LinearLayout(context).apply { orientation = HORIZONTAL }

        init {
            orientation = VERTICAL
            setPadding(context.dp(16), context.dp(5), context.dp(16), context.dp(5))
            val card = LinearLayout(context).apply {
                orientation = VERTICAL
                background = context.box(Night.charcoal, Night.border, 12)
                setPadding(context.dp(14), context.dp(12), context.dp(14), context.dp(12))
            }
            val top = LinearLayout(context).apply { orientation = HORIZONTAL }
            top.addView(title, lp(0, WRAP, 1f))
            top.addView(tag, lp(WRAP, WRAP).margins(l = context.dp(8)))
            card.addView(top, lp())
            card.addView(summary, lp().margins(t = context.dp(4)))
            card.addView(meta, lp().margins(t = context.dp(8)))
            addView(card, lp())
        }

        fun bind(e: Entry) {
            title.text = e.name
            tag.text = when {
                e.branches.size >= 4 -> "ALL BRANCHES"
                else -> e.branches.joinToString(" / ") { Branches.short(it).uppercase() }
            }
            summary.text = e.summary
            meta.removeAllViews()
            meta.addView(context.proofChip(e.proof), lp(WRAP, WRAP).margins(r = context.dp(6)))
            meta.addView(context.pill(e.group), lp(WRAP, WRAP).margins(r = context.dp(6)))
            e.years()?.let { meta.addView(context.pill(it), lp(WRAP, WRAP)) }
        }
    }
}
