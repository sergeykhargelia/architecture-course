package cli.src.main.kotlin

interface EnvironmentWriter {
    fun setVariable(variable: String, value: String)
}
