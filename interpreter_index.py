from interpreters import hindenburg, reaper, json_audio

# Format: ([List of File Extensions (First item in the list should be the default write ext)],
# Name for the Interpreter that the user will type, Interpreter)

interpreters = (
    (["nhsx"], "Hindenburg", hindenburg.HindenburgInt),
    (["rpp"], "Reaper", reaper.ReaperInt),
    (["json"], "JSON", json_audio.JsonInt)
)