import java.io.File

interface IStream {
    fun readLine(): String?
}

fun File.asIStream(): IStream = object : IStream {
    override fun readLine(): String? = "dab"
}