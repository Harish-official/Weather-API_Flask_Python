from flask import Flask,render_template,request,redirect,url_for
import requests,datetime

app = Flask(__name__)

def DateString():
    x = datetime.datetime.now()
    day = x.strftime("%A")
    date = x.strftime("%d")
    year = x.year
    month = x.strftime("%B")
    return f"{day}, {date} {month} {year}"

@app.route("/",methods=["GET","POST"])
def Home():
    def WeatherResponse(city_name):
        API_KEY = "f3cc4b19de1bc31ec100899781f411c3"
        URL = f"https://api.openweathermap.org/data/2.5/weather"

        weather_params = {
            "q":f"{city_name}",
            "appid":f"{API_KEY}"
        }
        response = requests.get(URL,params = weather_params)
        if response.status_code>399:
            return "error"
        else:
            response = response.json()
        temperature = response["main"]["temp"]
        weather = response["weather"][0]["main"]
        country = response["sys"]["country"]
        report = {
            "temp": round(temperature-273),
            "weather": weather,
            "city": city_name,
            "country": country
        }
        return report
    if request.method=="POST":
        city_name = request.form["city-name"]
        response = WeatherResponse(city_name)
        if response=="error":
            return render_template("error.html")
        else:
            return render_template("index.html",report=response,date_string = DateString())
    else:
        city_name = "Mumbai"
        response = WeatherResponse(city_name)     
    return render_template("index.html",report = response,date_string = DateString())


if __name__=="__main__":
    app.run(debug=True)