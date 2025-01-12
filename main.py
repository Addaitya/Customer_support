from tools.excursion import search_trip_recommendations

res = search_trip_recommendations.invoke(
    input="",
    config={
    "configurable": {
        "passenger_id": '8675 588663'
    }
    }
)

print(res)