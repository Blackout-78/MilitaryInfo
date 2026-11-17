package com.militaryinfo.app

enum class Proof(val key: String, val label: String) {
    OFFICIAL("official", "Official"),
    HISTORICAL("historical", "Historical"),
    UNVERIFIED("unverified", "Unverified");

    companion object {
        fun fromKey(key: String?): Proof =
            entries.firstOrNull { it.key == key } ?: UNVERIFIED
    }
}

enum class Tab(
    val key: String,
    val barLabel: String,
    val title: String,
    val searchHint: String,
    val icon: Int
) {
    UNIFORMS("uniforms", "Uniforms", "Uniforms", "Search BDU, Woodland, pinks and greens", R.drawable.ic_shirt),
    MEDALS("medals", "Medals", "Medals and ribbons", "Search medal, ribbon, device", R.drawable.ic_medal),
    BADGES("badges", "Badges", "Badges and devices", "Search sharpshooter, airborne, bar", R.drawable.ic_shield),
    RANKS("ranks", "Ranks", "Patches and ranks", "Search sergeant, stripes, tab, patch", R.drawable.ic_chevrons_up),
    SETTINGS("settings", "Settings", "Settings", "", R.drawable.ic_settings)
}

object Eras {
    val all: List<Pair<String, String>> = listOf(
        "ww1" to "WWI",
        "interwar" to "Interwar",
        "ww2" to "WWII",
        "korea" to "Korea",
        "vietnam" to "Vietnam",
        "coldwar" to "Cold War",
        "gulf" to "Gulf War",
        "modern" to "Modern"
    )

    fun label(key: String): String = all.firstOrNull { it.first == key }?.second ?: key
}

object Branches {
    val all: List<String> = listOf("Army", "Navy", "Marine Corps", "Air Force", "Coast Guard", "Space Force")

    fun short(branch: String): String = if (branch == "Marine Corps") "Marines" else branch
}

data class Swatch(val role: String, val name: String, val hex: String)

data class Variant(
    val label: String,
    val finish: String?,
    val gender: String?,
    val uniform: String?,
    val era: String?,
    val note: String?,
    val swatches: List<Swatch>,
    val image: String?
)

data class Attachment(
    val name: String,
    val note: String?,
    val variants: List<Variant>,
    val link: String? = null
)

data class Entry(
    val id: String,
    val tab: String,
    val group: String,
    val name: String,
    val branches: List<String>,
    val eras: List<String>,
    val yearFrom: Int?,
    val yearTo: Int?,
    val summary: String,
    val facts: List<String>,
    val remember: String?,
    val swatches: List<Swatch>,
    val variants: List<Variant>,
    val attachments: List<Attachment>,
    val proof: Proof,
    val sources: List<String>,
    val image: String?
) {
    fun years(): String? = when {
        yearFrom != null && yearTo != null -> "$yearFrom to $yearTo"
        yearFrom != null -> "$yearFrom to today"
        else -> null
    }

    fun matches(tokens: List<String>): Boolean {
        if (tokens.isEmpty()) return true
        val hay = buildString {
            append(name).append(' ').append(group).append(' ').append(summary).append(' ')
            append(remember.orEmpty()).append(' ')
            facts.forEach { append(it).append(' ') }
            branches.forEach { append(it).append(' ') }
            eras.forEach { append(Eras.label(it)).append(' ') }
            variants.forEach { v ->
                append(v.label).append(' ').append(v.finish.orEmpty()).append(' ')
                append(v.uniform.orEmpty()).append(' ').append(v.note.orEmpty()).append(' ')
            }
            attachments.forEach { a ->
                append(a.name).append(' ')
                a.variants.forEach { v -> append(v.label).append(' ').append(v.finish.orEmpty()).append(' ') }
            }
        }.lowercase()
        return tokens.all { hay.contains(it) }
    }

    fun matchesGender(gender: String?): Boolean {
        if (gender == null) return true
        val tagged = variants.mapNotNull { it.gender }
        if (tagged.isEmpty()) return true
        return tagged.any { it == gender || it == "any" }
    }
}
