import org.junit.jupiter.api.Assertions.*
import java.io.File
import java.nio.file.Paths

class CatCommandTest {
    @org.junit.jupiter.api.Test
    fun `test cat with no arguments`() {
        val outputBuffer = StringBuilder()
        val inputFileText = object {}::class.java.getResource("statement.txt").readText()
        val command = CatCommand(
            inputFileText.asIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf()
        )
        command.execute()
        assertEquals(inputFileText, outputBuffer.toString())
    }

    @org.junit.jupiter.api.Test
    fun `test cat with filename as an argument`() {
        fun joinPaths(prefix: String, suffix: String): String {
            return Paths.get(prefix, suffix).toString()
        }
        val outputBuffer = StringBuilder()
        val fileName = "statement.txt"
        val resourcesPath = Paths.get("src", "test", "resources").toString()
        val command = CatCommand(
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf(joinPaths(resourcesPath, fileName))
        )
        command.execute()
        val inputFileText = object {}::class.java.getResource(fileName).readText()
        assertEquals(inputFileText, outputBuffer.toString())
    }
}