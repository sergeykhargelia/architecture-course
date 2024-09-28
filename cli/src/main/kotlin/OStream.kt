import java.io.File

interface OStream {
    fun writeLine(s: String)
}

fun StringBuilder.asOStream(): OStream = object : OStream {
    override fun writeLine(s: String) {
        if (this@asOStream.isNotEmpty()) {
            this@asOStream.append("\n")
        }
        this@asOStream.append(s)
    }
}