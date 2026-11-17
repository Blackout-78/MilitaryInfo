package com.militaryinfo.app

import android.app.Activity
import android.os.Bundle
import android.view.Gravity
import android.view.View
import android.widget.FrameLayout
import android.widget.ImageView
import android.widget.LinearLayout

class MainActivity : Activity() {

    private var entries: List<Entry> = emptyList()
    private var loadError: String? = null
    private val screens = HashMap<Tab, View>()
    private val buttons = HashMap<Tab, TabButton>()
    private lateinit var host: FrameLayout
    private var current = Tab.UNIFORMS
    private var detailOpen = false
    private val trail = ArrayList<Entry>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            entries = Repository.load(this)
        } catch (e: Exception) {
            loadError = e.message ?: e.javaClass.simpleName
        }
        setContentView(buildRoot())
        showTab(Tab.UNIFORMS)
    }

    private fun buildRoot(): View {
        val root = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setBackgroundColor(Night.navy)
        }

        host = FrameLayout(this)
        val content = FrameLayout(this)
        content.addView(host, FrameLayout.LayoutParams(MATCH, MATCH))

        val stamp = label("v${BuildConfig.VERSION_NAME} build ${BuildConfig.VERSION_CODE}", 10f, Night.muted)
        root.addView(content, lp(MATCH, 0, 1f))
        stamp.setPadding(dp(10), dp(2), 0, dp(3))
        root.addView(stamp, lp())

        val divider = View(this).apply { setBackgroundColor(Night.border) }
        root.addView(divider, lp(MATCH, 1))

        val bar = LinearLayout(this).apply {
            orientation = LinearLayout.HORIZONTAL
            setBackgroundColor(Night.charcoal)
        }
        Tab.entries.forEach { tab ->
            val b = TabButton(tab)
            buttons[tab] = b
            bar.addView(b, lp(0, WRAP, 1f))
        }
        root.addView(bar, lp())
        return root
    }

    private fun emptyText(): String =
        loadError?.let { "Could not load data: $it" } ?: "No matches. Clear a filter or try another word."

    private fun screenFor(tab: Tab): View = screens.getOrPut(tab) {
        if (tab == Tab.SETTINGS) SettingsView(this, entries, loadError)
        else CatalogView(this, tab, entries,
            if (tab == Tab.PATCHES && entries.none { it.tab == tab.key } && loadError == null) "Unit patches are being added. Check Releases for updates." else emptyText()) { openDetail(it) }
    }

    private fun showTab(tab: Tab) {
        current = tab
        detailOpen = false
        trail.clear()
        Tab.entries.forEach { buttons[it]?.setActive(it == tab) }
        host.removeAllViews()
        host.addView(screenFor(tab), FrameLayout.LayoutParams(MATCH, MATCH))
    }

    private fun openDetail(entry: Entry, push: Boolean = true) {
        if (push) trail.add(entry)
        detailOpen = true
        host.removeAllViews()
        host.addView(
            DetailView(this, entry, entries, { openDetail(it) }) { goBack() },
            FrameLayout.LayoutParams(MATCH, MATCH)
        )
    }

    private fun goBack() {
        if (trail.size > 1) {
            trail.removeAt(trail.size - 1)
            openDetail(trail.last(), push = false)
        } else {
            trail.clear()
            showTab(current)
        }
    }

    @Suppress("DEPRECATION", "OVERRIDE_DEPRECATION")
    override fun onBackPressed() {
        if (detailOpen) goBack() else super.onBackPressed()
    }

    private inner class TabButton(private val tab: Tab) : LinearLayout(this@MainActivity) {
        private val pill = FrameLayout(context)
        private val icon = ImageView(context)
        private val text = label(tab.barLabel, 11f, Night.muted)

        init {
            orientation = VERTICAL
            gravity = Gravity.CENTER_HORIZONTAL
            setPadding(0, dp(8), 0, dp(10))
            isClickable = true
            icon.setImageResource(tab.icon)
            pill.setPadding(dp(16), dp(3), dp(16), dp(3))
            pill.addView(icon, FrameLayout.LayoutParams(dp(24), dp(24)))
            addView(pill, lp(WRAP, WRAP))
            addView(text, lp(WRAP, WRAP).margins(t = dp(2)))
            setOnClickListener { showTab(tab) }
            setActive(false)
        }

        fun setActive(active: Boolean) {
            if (active) {
                pill.background = box(Night.raised, null, 20)
                icon.setColorFilter(Night.accent)
                text.setTextColor(Night.text)
            } else {
                pill.background = null
                icon.setColorFilter(Night.muted)
                text.setTextColor(Night.muted)
            }
        }
    }
}
