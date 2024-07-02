# from langchain_experimental.sql import SQLDatabaseChain
# import model
# import sql_connection
# import fetching_query_data

# import time
# from flask import Flask, render_template, redirect, url_for, jsonify, request


# app = Flask(__name__)


# @app.route("/")
# def welcome():
#     return "<h1> hello prompt</h1>"


# error_message = {"text": "Data doesn't exist for this Query...<br>Try with new query"}

# start_time = time.time()


# llm = model.getmodel()
# db = sql_connection.return_database(sql_connection.connection_string)


# @app.route("/prompt", methods=["GET", "POST"])
# def get_prompt():
#     if request.method == "POST":
#         text = request.form["prompt"]

#         db_chain = SQLDatabaseChain.from_llm(
#             llm=llm, db=db, verbose=True, return_sql=True
#         )

#         inst = db_chain(text)

#         data = fetching_query_data.query_to_df(inst, sql_connection.mssql_conn, 200)

#         for data_chunk in data:
#             data_chunk = fetching_query_data.data_preprocessing(data_chunk)
#             print(f"data shape::::{data_chunk.shape}\n\n\n")
#             json_data = data_chunk.to_json(orient="split")
#             yield json_data
#             return render_template("form.html", json_data=json_data, error=None)

#     return render_template(
#         "form.html", json_data=None, error=None, time=time.time() - start_time
#     )


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, Response, request, jsonify
import time
import json
import model
import sql_connection
import fetching_query_data
from langchain_experimental.sql import SQLDatabaseChain


app = Flask(__name__)


@app.route("/")
def welcome():
    return "<h1> hello prompt</h1>"


error_message = {"text": "Data doesn't exist for this Query...<br>Try with new query"}

start_time = time.time()

llm = model.get_model()
db = sql_connection.return_database(sql_connection.connection_string)


def generate_data_chunks(data):
    for data_chunk in data:
        data_chunk = fetching_query_data.data_preprocessing(data_chunk)
        print(f"data shape::::{data_chunk.shape}\n\n\n")
        json_data = data_chunk.to_json(orient="split")
        print(f"type of data_chunk {type(data_chunk)}")

        print(f"type of json_data {type(json_data)}")

        yield json_data


@app.route("/prompt", methods=["GET", "POST"])
def get_prompt():
    if request.method == "POST":
        text = request.form["prompt"]

        db_chain = SQLDatabaseChain.from_llm(
            llm=llm, db=db, verbose=True, return_sql=True
        )

        inst = db_chain(text)

        data = fetching_query_data.query_to_df(inst, sql_connection.mssql_conn, 200)

        return Response(generate_data_chunks(data), content_type="application/json")

    return render_template("form.html", json_data=None, error=None)


if __name__ == "__main__":
    app.run(debug=True)
