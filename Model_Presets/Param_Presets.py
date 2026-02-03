PARAM_PRESETS = {

    "Default" : {
        "temp" : 0.90,
        "topP" : 0.90,
        "repeat_penalty" : 1.10,
        "topK" : 40
    },
    
    "Tool Execution" : {
        "temp" : 0.25,
        "topP" : 0.85,
        "repeat_penalty" : 1.00,
        "topK" : 30
    },

    "Creative": {
        "temp": 1.60,
        "topP": 0.98,
        "repeat_penalty": 0.95,
        "topK": 80
    },

    "Strict": {
        "temp": 0.10,
        "topP": 0.70,
        "repeat_penalty": 1.05,
        "topK": 20
    },

}