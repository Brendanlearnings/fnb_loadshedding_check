from datetime import datetime, timedelta, timezone
import json
import logging

from flask import Flask, Response, request
from load_shedding.load_shedding import get_schedule, StageError
from load_shedding.providers.eskom import Eskom, Suburb, Province, Stage, ProviderError

logging.basicConfig(filename='../load-shedding.log', level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def main():
    suburb_id = request.args.get("suburb_id")
    province_id = request.args.get("province_id")
    stage = request.args.get("stage")
    if suburb_id and province_id and stage:
        suburb = Suburb(id=suburb_id)
        province = Province(int(province_id))
        stage = Stage(int(stage))

        try:
            logging.log(logging.INFO, "Getting info for suburb: {suburb_id}".format(suburb_id=suburb.id))
            provider = Eskom()
            schedule = get_schedule(provider, province=province, suburb=suburb, stage=stage)
            logging.log(logging.INFO, "Schedule for {suburb_id} {stage}: {schedule}".format(
                suburb_id=suburb.id,
                stage=stage,
                schedule=schedule
            ))

            tz = timezone.utc
            days = 7
            forecast = []
            for s in schedule:
                start = datetime.fromisoformat(s[0])
                end = datetime.fromisoformat(s[1])
                if start.date() > datetime.now(tz).date() + timedelta(days=days):
                    continue
                if end < datetime.now(tz):
                    continue
                forecast.append({"start": start.isoformat(), "end": end.isoformat()})

        except (ProviderError, StageError) as e:
            return Response(json.dumps(str(e)), mimetype='application/json')
        else:
            return Response(json.dumps(forecast), mimetype='application/json')

    suburb = request.args.get("suburb")
    if suburb:
        try:
            eskom = Eskom()
            suburbs = eskom.find_suburbs(search_text=suburb)
            logging.log(logging.INFO, "Searching suburbs for {suburb}: {suburbs}".format(
                suburb=str(suburb),
                suburbs=",".join([str(suburb) for suburb in suburbs])
            ))
            schedule = get_schedule(eskom, province=suburbs[0].province, suburb=suburbs[0], stage=Stage.STAGE_2)
            logging.log(logging.INFO, "Schedule for {suburb} ({suburb_id}): {schedule}".format(
                suburb=str(suburb),
                suburb_id=suburbs[0].id,
                schedule=schedule
            ))
            return Response(json.dumps(schedule), mimetype='application/json')
        except ProviderError as e:
            return Response(json.dumps(str(e)), mimetype='application/json')
        else:
            return Response(json.dumps(schedule), mimetype='application/json')

    index = "Try <a href='/?suburb=Milnerton'>/?suburb=Milnerton</a>" \
            " or <a href='/?suburb_id=1058852&province_id=9&stage=2'>/?suburb_id=1058852&province_id=9&stage=2</a> "
    return Response(index, status=400)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
