package com.militaryinfo.app

import android.content.Context
import org.json.JSONArray
import org.json.JSONObject

object Repository {

    const val DATA_FILE = "data/entries.json"

    fun load(context: Context): List<Entry> {
        val text = context.assets.open(DATA_FILE).bufferedReader().use { it.readText() }
        val arr = JSONObject(text).getJSONArray("entries")
        return List(arr.length()) { parseEntry(arr.getJSONObject(it)) }
    }

    private fun JSONObject.str(key: String): String? =
        if (has(key) && !isNull(key)) getString(key) else null

    private fun JSONObject.int(key: String): Int? =
        if (has(key) && !isNull(key)) getInt(key) else null

    private fun JSONObject.strings(key: String): List<String> {
        val a = optJSONArray(key) ?: return emptyList()
        return List(a.length()) { a.getString(it) }
    }

    private fun swatches(a: JSONArray?): List<Swatch> {
        if (a == null) return emptyList()
        return List(a.length()) {
            val o = a.getJSONObject(it)
            Swatch(o.getString("role"), o.getString("name"), o.getString("hex"))
        }
    }

    private fun variants(a: JSONArray?): List<Variant> {
        if (a == null) return emptyList()
        return List(a.length()) {
            val o = a.getJSONObject(it)
            Variant(
                label = o.getString("label"),
                finish = o.str("finish"),
                gender = o.str("gender"),
                uniform = o.str("uniform"),
                era = o.str("era"),
                note = o.str("note"),
                swatches = swatches(o.optJSONArray("swatches")),
                image = o.str("image")
            )
        }
    }

    private fun attachments(a: JSONArray?): List<Attachment> {
        if (a == null) return emptyList()
        return List(a.length()) {
            val o = a.getJSONObject(it)
            Attachment(o.getString("name"), o.str("note"), variants(o.optJSONArray("variants")))
        }
    }

    private fun parseEntry(o: JSONObject): Entry = Entry(
        id = o.getString("id"),
        tab = o.getString("tab"),
        group = o.getString("group"),
        name = o.getString("name"),
        branches = o.strings("branches"),
        eras = o.strings("eras"),
        yearFrom = o.int("yearFrom"),
        yearTo = o.int("yearTo"),
        summary = o.getString("summary"),
        facts = o.strings("facts"),
        remember = o.str("remember"),
        swatches = swatches(o.optJSONArray("swatches")),
        variants = variants(o.optJSONArray("variants")),
        attachments = attachments(o.optJSONArray("attachments")),
        proof = Proof.fromKey(o.str("proof")),
        sources = o.strings("sources"),
        image = o.str("image")
    )
}
