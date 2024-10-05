import org.junit.jupiter.api.Assertions.*
import java.nio.file.Paths

class WCCommandTest {
    @org.junit.jupiter.api.Test
    fun `test wc with no arguments, emulating scenario with pipes`() {
        val outputBuffer = StringBuilder()
        val inputFileText = object {}::class.java.getResource("statement.txt").readText()
        val command = WCCommand(
            inputFileText.asIStream(),
            outputBuffer.asOStream(),
            StringBuilder().asOStream(),
            listOf()
        )
        command.execute()
        assertEquals("     1    31   185", outputBuffer.toString())
    }

    @org.junit.jupiter.api.Test
    fun `test wc with filename as an argument`() {
        val outputBuffer = StringBuilder()
        val fileName = "statement.txt"
        val resourcesPath = Paths.get("src", "test", "resources").toString()
        val inputFilePath = joinPaths(resourcesPath, fileName)
        val command = WCCommand(
            MockIStream(),
            outputBuffer.asOStream(),
            MockOStream(),
            listOf(inputFilePath)
        )
        command.execute()
        assertEquals("     1    31   185 $inputFilePath", outputBuffer.toString())
    }
}