import java.nio.file.Paths

fun joinPaths(prefix: String, suffix: String): String {
    return Paths.get(prefix, suffix).toString()
}