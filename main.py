import back
from maindash import app
import front


if __name__ == '__main__':
    back.create_test_table(back.get_conn())
    app.layout = front.get_layout()
    app.run_server(debug=True, host="localhost", port="8050")
