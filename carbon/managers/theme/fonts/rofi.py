
def updateRofi(font: str) -> str:

    base = f"""
// NOTE: This file is written by carbon shell
* {{
    fontTextSmall:                   "{font} 11";
    fontText:                        "{font} 13";
    fontTextBig:                     "{font} 15";
    fontTextBigger:                  "{font} 20";
    fontTextBiggest:                 "{font} 26";
    fontTextLarge:                   "{font} 36";
    fontTextHuge:                    "{font} 96";

    font: @fontText;
}}
"""
    return base