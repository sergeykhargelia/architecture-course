import java.util.LinkedList
import java.util.Queue

class Buffer: IStream, OStream {
    private val lines: Queue<String> = LinkedList()

    override fun readLine(): String? {
        return lines.poll()
    }

    override fun writeLine(s: String) {
        lines.add(s)
    }
}