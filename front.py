from dash import html, dcc, Input, Output, State, dash_table
import back
from maindash import app


def get_layout():
    return html.Div([
            html.H1('Web Application connected to a Live Database', style={'textAlign': 'center'}),
            dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
            html.Div(id='mongo-datatable', children=[]),
            dcc.Store(id='changed-cell')
        ])


@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals')
              )
def populate_datatable(n_intervals):
    df = back.get_table(back.get_conn())
    df_tags = df[["id", "tag_1", "tag_2", "tag_3",
                  "tag_1_relevance", "tag_2_relevance", "tag_3_relevance"]]
    return [
        dash_table.DataTable(
                id='our-table',
                data=df_tags.to_dict('records'),
                columns=[{'id': p, 'name': p, 'editable': True} if "relevance" in p
                         else {'id': p, 'name': p, 'editable': False}
                         for p in df_tags],
        )
    ]


app.clientside_callback(
    """
    function (input,oldinput) {
        if (oldinput != null) {
            if(JSON.stringify(input) != JSON.stringify(oldinput)) {
                for (i in Object.keys(input)) {
                    newArray = Object.values(input[i])
                    oldArray = Object.values(oldinput[i])
                    if (JSON.stringify(newArray) != JSON.stringify(oldArray)) {
                        entNew = Object.entries(input[i])
                        entOld = Object.entries(oldinput[i])
                        for (const j in entNew) {
                            if (entNew[j][1] != entOld[j][1]) {
                                changeRef = [i, entNew[j][0]] 
                                break        
                            }
                        }
                    }
                }
            }
            return changeRef
        }
    }    
    """,
    Output('changed-cell', 'data'),
    Input('our-table', 'data'),
    State('our-table', 'data_previous')
)


@app.callback(
    Input("changed-cell", "data"),
    Input("our-table", "data"),
)
def update_d(cc, tabledata):
    if cc:
        print(f'changed cell: {cc}')
        print(f'Current DataTable: {tabledata}')
        x = int(cc[0])

        row_id = tabledata[x]['id']
        col_id = cc[1]
        new_cell_data = tabledata[x][col_id]
        cursor = conn.cursor()
        sql_update = f"""UPDATE test_table
                        SET {col_id} = {new_cell_data}
                        WHERE id == {row_id}"""
        cursor.execute(sql_update)

    return 0