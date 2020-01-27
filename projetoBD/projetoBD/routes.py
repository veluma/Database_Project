from flask import render_template, url_for, flash, redirect, request
from projetoBD import app, db
from sqlalchemy import func, create_engine
from projetoBD.models import Locais, Restaurante, Cliente, Localconsumo, Funcionario, TipoEmenta, TipoRefeicao, Consumo, TipoItem,Item, DataEmenta, Ementa, Alergia, ItenAlergia, EmentaItem

engine = create_engine('postgresql://postgres:1304@localhost/ProjetoBD2')
connection = engine.connect()

@app.route("/")
@app.route("/home")
def home():
	records= connection.execute('SELECT * from selectrestaurante')
	return render_template('home.html',title='Home', records=records)
   

@app.route("/restaurante/<int:id_restaurante><string:nome_ident>")
def restaurante(id_restaurante, nome_ident):
    return render_template('restaurante.html', title='Restaurante', id_restaurante=id_restaurante, nome_ident=nome_ident)


@app.route("/rest_id/<int:id_restaurante>")
def rest_id(id_restaurante):
    sql_string = """
        SELECT * from selectementa({id});
    """.format(id=id_restaurante)
    records= connection.execute(sql_string)
    return render_template('rest_id.html', title='Ementa', records=records, id_restaurante=id_restaurante)


@app.route("/ementa_data/<int:id_restaurante><int:id_dataementa><string:data_ementa>")
def ementa_data(id_restaurante, id_dataementa, data_ementa):
    sql_string = """
        SELECT public.xml_function({id_rest},{id});
    """.format(id=id_dataementa, id_rest=id_restaurante)
    records= connection.execute(sql_string)
    return render_template('ementa_data.html',title='Filtro por Data', records=records, data_ementa=data_ementa, id_restaurante=id_restaurante, id_dataementa=id_dataementa)


@app.route("/ementa_id/<int:id_tipoementa><int:id_restaurante>")
def ementa_id(id_tipoementa, id_restaurante):
    sql_string = """
        SELECT * from selectitem({id},{id_rest});
    """.format(id=id_tipoementa, id_rest=id_restaurante)
    records= connection.execute(sql_string)
    return render_template('ementa_id.html',title='Filtro por Tipo Ementa', records = records, id_tipoementa =id_tipoementa, id_restaurante=id_restaurante)



@app.route("/item_alergia/<int:id_item>")
def item_alergia(id_item):
    sql_string = """
        SELECT * from selec_alergia({id});
    """.format(id=id_item)
    records= connection.execute(sql_string)
    return render_template('item_alergia.html',title='Item Alergia', records=records, id_item=id_item)


@app.route("/funcionario/<int:id_restaurante>")
def funcionario(id_restaurante):
    sql_string = """
        SELECT * from selec_funcionario({id});
    """.format(id=id_restaurante)
    records= connection.execute(sql_string)
    return render_template('funcionario.html', title='Funcionario', records=records, id_restaurante=id_restaurante)

@app.route("/inserir_func/<int:id_restaurante>", methods=['GET', 'POST'])
def inserir_func(id_restaurante):
    edits = Funcionario()
    if request.method == 'POST':
        edits.nome = request.form['nome']
        edits.id_localconsumo = request.form['id_consumo']
        edits.id_restaurante = id_restaurante
        sql_string= """
            CALL public.insert_func('{nome}', {id}, {id_localconsumo});   
        """.format(id=edits.id_restaurante, nome=edits.nome, id_localconsumo=edits.id_localconsumo)
        db.session.execute(sql_string) 
        db.session.commit() 
        return redirect(url_for('funcionario', id_restaurante=id_restaurante))

    else:
        return render_template('inserir_func.html', title='Inserir Funcionario', id_restaurante=id_restaurante, edits = edits)


@app.route("/editados/<int:id_restaurante>")
def editados(id_restaurante):
    sql_string= """
        SELECT * from selec_funcionario({id});
    """.format(id=id_restaurante)
    records= connection.execute(sql_string)
    antigos= connection.execute('SELECT * from select_alteracao')
    return render_template('editados.html', title='Editados', antigos=antigos, records=records, id_restaurante=id_restaurante)


@app.route("/editar_func/<int:id_funcionario><string:nome><int:id_restaurante>", methods=['GET', 'POST'])
def editar_func(id_funcionario, nome, id_restaurante):
    edits = Funcionario.query.filter_by(id_funcionario=id_funcionario).one()
    if request.method == 'POST':
        if request.form['nome']:
            edits.nome = request.form['nome']
            edits.id_localconsumo = request.form['id_consumo']
            sql_string= """
                CALL public.update_func('{nome}', {id} ,{id_local});   
            """.format(id=id_funcionario, nome=edits.nome, id_local=edits.id_localconsumo)
            db.session.execute(sql_string) 
            db.session.commit() 
            flash('Your account has been updated!', 'success')
        return redirect(url_for('editados', id_restaurante=id_restaurante))
    else:
        return render_template('editar_func.html', title='Funcionario',id_funcionario=id_funcionario, nome=nome, edits = edits)

@app.route("/deletar_func/<int:id_funcionario><int:id_restaurante>")
def deletar_func(id_funcionario, id_restaurante):
    sql_string= """
                CALL public.deletar_func({id});   
            """.format(id=id_funcionario)
    db.session.execute(sql_string) 
    db.session.commit() 
    return redirect(url_for('funcionario', id_restaurante=id_restaurante))


@app.route("/consumo/<int:id_restaurante>")
def consumo(id_restaurante):
    sql_string = """
        SELECT * from select_consumo({id});
    """.format(id=id_restaurante)
    records= connection.execute(sql_string)
    return render_template('consumo.html', title='Consumo', records=records, id_restaurante=id_restaurante)


