interface OStream {
    fun writeLine(s: String)
}

fun stdoutAsOStream(): OStream = object : OStream {
    override fun writeLine(s: String) {
        println(s)
    }
}

fun StringBuilder.asOStream(): OStream = object : OStream {
    override fun writeLine(s: String) {
        if (this@asOStream.isNotEmpty()) {
            this@asOStream.append("\n")
        }
        this@asOStream.append(s)
    }
}