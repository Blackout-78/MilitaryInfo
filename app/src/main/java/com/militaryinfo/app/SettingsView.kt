package com.militaryinfo.app

import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.view.Gravity
import android.widget.LinearLayout
import android.widget.ScrollView
import android.widget.Toast

object AppInfo {
    const val NAME = "MilitaryInfo"
    // Change this one line if the GitHub repo name differs.
    const val RELEASES_URL = "https://github.com/Blackout-78/MilitaryInfo/releases"
}

class SettingsView(
    context: Context,
    entries: List<Entry>,
    loadError: String?
) : ScrollView(context) {

    init {
        isVerticalScrollBarEnabled = false
        val body = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(context.dp(16), context.dp(8), context.dp(16), context.dp(40))
        }
        body.addView(context.label("Settings", 22f, medium = true), lp().margins(b = context.dp(14)))

        body.addView(
            card(
                context, "Version",
                context.label("${AppInfo.NAME} ${BuildConfig.VERSION_NAME} (build ${BuildConfig.VERSION_CODE})", 15f, medium = true),
                context.label("Army, Navy, and ranks for Marines, Air Force, Space Force, and Coast Guard loaded. Two older uniforms are unverified samples.", 13f, Night.muted)
            ),
            lp().margins(b = context.dp(10))
        )

        val button = context.label("Open GitHub Releases", 14f, Night.navy, medium = true).apply {
            gravity = Gravity.CENTER
            background = context.box(Night.accent, null, 10)
            setPadding(context.dp(12), context.dp(12), context.dp(12), context.dp(12))
            setOnClickListener { openReleases(context) }
        }
        body.addView(
            card(
                context, "Updates", button,
                context.label("The app stays offline. Updates install only from GitHub.", 12f, Night.muted)
            ),
            lp().margins(b = context.dp(10))
        )

        val counts = Proof.entries.joinToString("   ") { p ->
            "${p.label}: ${entries.count { it.proof == p }}"
        }
        val dataViews = mutableListOf(
            context.label("${entries.size} entries", 15f, medium = true),
            context.label(counts, 13f, Night.muted)
        )
        if (loadError != null) dataViews.add(context.label("Load error: $loadError", 13f, Night.muted))
        body.addView(card(context, "Data", *dataViews.toTypedArray()), lp().margins(b = context.dp(10)))

        body.addView(
            card(
                context, "Proof tags",
                context.label("Official: confirmed by a regulation or the Institute of Heraldry.", 13f),
                context.label("Historical: confirmed by documented history, such as archives and museum records.", 13f),
                context.label("Unverified: no source yet. Kept out of the final database.", 13f)
            ),
            lp().margins(b = context.dp(10))
        )

        body.addView(
            card(
                context, "About",
                context.label("Offline and private. No internet permission, no accounts, no tracking.", 13f),
                context.label("Icons by Tabler Icons, MIT license.", 12f, Night.muted)
            ),
            lp()
        )
        addView(body, lp())
    }

    private fun card(context: Context, title: String, vararg rows: android.view.View): LinearLayout {
        val c = LinearLayout(context).apply {
            orientation = LinearLayout.VERTICAL
            background = context.box(Night.charcoal, Night.border, 12)
            setPadding(context.dp(14), context.dp(12), context.dp(14), context.dp(12))
        }
        c.addView(context.label(title, 12f, Night.muted))
        rows.forEach { c.addView(it, lp().margins(t = context.dp(6))) }
        return c
    }

    private fun openReleases(context: Context) {
        try {
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(AppInfo.RELEASES_URL)))
        } catch (e: ActivityNotFoundException) {
            Toast.makeText(context, "No browser found on this phone", Toast.LENGTH_LONG).show()
        }
    }
}
