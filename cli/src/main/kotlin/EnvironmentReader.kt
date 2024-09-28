package cli.src.main.kotlin

interface EnvironmentReader {
    fun getVariable(variable: String): String
}
