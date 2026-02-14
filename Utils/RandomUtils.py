

#Formats text to a certain width
def format_text(text, width):
        return "<br>".join([text[i:i+width] for i in range(0, len(text), width)])