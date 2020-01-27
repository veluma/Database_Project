from datetime import datetime
from projetoBD import db


class Locais(db.Model):
    """docstring for User"""
    id_local = db.Column(db.Integer, primary_key = True)
    distritos = db.Column(db.String(50), unique=False)
    freguesia= db.Column(db.String(50), unique=False)
    addresses = db.relationship('Restaurante', backref='locais', lazy=True)

    def __repr__(self):
        return f"Locais('{self.distrito}', '{self.freguesia}')"

class Restaurante(db.Model):
    """docstring for Restaurante"""
    id_restaurante = db.Column(db.Integer, primary_key = True)
    morada = db.Column(db.String(80), unique=False)
    nome_ident = db.Column(db.String(50), unique=False)
    id_local = db.Column(db.Integer, db.ForeignKey('locais.id_local'), nullable=False) 
        
    def __repr__(self):
        return f"Restaurante('{self.id_restaurante}' ,'{self.morada}','{self.nome_ident}')"
        

class Localconsumo(db.Model):
    """docstring for Localconsumo"""
    id_localconsumo = db.Column(db.Integer, primary_key = True)
    designacao = db.Column(db.String(200), unique=False)
    id_restaurante = db.Column(db.Integer, db.ForeignKey('restaurante.id_restaurante'), nullable=False)

    id_consumo = db.relationship('Consumo', backref='localconsumo', lazy=True)
    id_funcionario = db.relationship('Funcionario', backref='localconsumo', lazy=True)

    def __repr__():
        return f"Localconsumo('{self.designacao}', '{self.id_restaurante}','{self.id_consumo}','{self.funcionario}')"

        
class Cliente(db.Model):
    """docstring for Cliente"""
    id_cliente = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(25), unique=False)
    nif = db.Column(db.String(10), unique=True)
    consumo = db.relationship('Consumo', backref='cliente', lazy=True)

    def __repr__():
        return f"Cliente('{self.nome}', '{self.nif}')"


class Funcionario(db.Model):
    """docstring for Funcionarios"""
    id_funcionario = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(256), unique=False)
    id_restaurante = db.Column(db.Integer, db.ForeignKey('restaurante.id_restaurante'), nullable=False)
    id_localconsumo = db.Column(db.Integer, db.ForeignKey('localconsumo.id_localconsumo'), nullable=False)
    
    id_consumo = db.relationship('Consumo', backref='funcionario', lazy=True)

    def __repr__():
        return f"Funcionario('{self.nome}', '{self.id_restaurante}', '{self.id_localconsumo}', '{self.id_localconsumo}')"


class TipoRefeicao(db.Model):
    """docstring for TipoRefeicao"""
    id_tiporefeicao = db.Column(db.Integer, primary_key = True)
    tipo_refeicao = db.Column(db.String(80), unique=False)
    
    #ementa = db.relationship('Ementa', backref='tiporefeicao', lazy=True)


    def __repr__():
        return f"TipoRefeicao('{self.tipo_refeicao}')"

class Consumo(db.Model):
    """docstring for Consumo"""
    id_consumo = db.Column(db.Integer, primary_key = True)
    data_consumo = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=False)
    id_localconsumo = db.Column(db.Integer, db.ForeignKey('localconsumo.id_localconsumo'), nullable=False)
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionario.id_funcionario'), nullable=False)
   
    item_consumo =db.relationship('item_consumo', backref='consumo', lazy=True)

    def __repr__():
        return f"Consumo('{self.data_consumo}', '{self.id_cliente}', '{self.id_localconsumo}', '{self.id_funcionario}')"



class TipoItem(db.Model):
    """docstring for TipoItem"""
    id_tipoitem = db.Column(db.Integer, primary_key = True)
    tipo_item = db.Column(db.String(50), unique=False)
    
    #id_item = db.relationship('Item', backref='tipoitem', lazy=True)


    def __repr__():
        return f"TipoItem('{self.id_tipoitem}', '{self.tipo_item}', '{self.id_item}')"

class TipoEmenta(db.Model):
    """docstring for TipoEmenta"""
    id_tipoementa = db.Column(db.Integer, primary_key = True)
    tipo_ementa = db.Column(db.String(30), unique=False)

    id_item = db.relationship('Item', backref='tipo_ementa', lazy=True)
    #id_ementa = db.relationship('Ementa', backref='tipoementa', lazy=True)

    def __repr__():
        return f"TipoEmenta('{self.tipo_ementa}')"

class Item(db.Model):
    """docstring for Itens"""
    id_item = db.Column(db.Integer, primary_key = True)
    designacao = db.Column(db.String(50), unique=False)
    preco = db.Column(db.Float, nullable=False)
    id_tipoementa = db.Column(db.Integer, db.ForeignKey('tipo_ementa.id_tipoementa'), nullable=False)

    ementaitens = db.relationship('EmentaItem', backref='item', lazy=True)
    alergia = db.relationship('ItenAlergia', backref='item', lazy=True)
    item_consumo =db.relationship('item_consumo', backref='item', lazy=True)

    def __repr__():
        return f"Item('{self.designacao}','{self.preco}', '{self.id_tipoementa}', '{self.ementaitens}', '{self.alergia}')"

class DataEmenta(db.Model):
    """docstring for DataEmenta"""
    id_dataementa = db.Column(db.Integer, primary_key = True)
    data_ementa = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    
    #ementa = db.relationship('Ementa', backref='dataementa', lazy=True)

    def __repr__():
        return f"DataEmenta('{self.data_ementa}', '{self.ementa}')"



class Ementa(db.Model):
    """docstring for Ementas"""
    id_ementa = db.Column(db.Integer, primary_key = True)
    id_tipoementa = db.Column(db.Integer, db.ForeignKey('TipoEmenta.id_tipoementa'), nullable=False)
    id_tiporefeicao = db.Column(db.Integer, db.ForeignKey('TipoRefeicao.id_tiporefeicao'), nullable=False)
    id_restaurante = db.Column(db.Integer, db.ForeignKey('restaurante.id_restaurante'), nullable=False)
    id_dataementa = db.Column(db.Integer, db.ForeignKey('DataEmenta.id_dataementa'), nullable=False)
    
    ementaitens = db.relationship('EmentaItem', backref='ementa', lazy=True)

    def __repr__():
        return f"Ementa('{self.id_tipoementa}','{self.id_tiporefeicao}', '{self.id_restaurante}', '{self.id_dataementa}', '{self.ementaitens}')"

class item_consumo(db.Model):
    id_item= db.Column(db.Integer, db.ForeignKey('item.id_item'), primary_key = True)
    id_consumo = db.Column(db.Integer, db.ForeignKey('consumo.id_consumo'), primary_key = True)
    qde = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)

    def __repr__():
        return f"item_consumo('{self.id_item}', '{self.id_consumo}', '{self.qde}', '{self.total}')"

class Alergia(db.Model):
    """docstring for Alergia"""
    id_alergia = db.Column(db.Integer, primary_key = True)
    detalhes = db.Column(db.String(100), unique=False) 
    
    alergia = db.relationship('ItenAlergia', backref='alergia', lazy=True)
 

    def __repr__():
        return f"Alergia('{self.detalhes}', '{self.alergia}')"


class ItenAlergia(db.Model):
    """docstring for ItenAlergia"""
    id_item = db.Column(db.Integer, db.ForeignKey('item.id_item'), primary_key = True)
    id_alergia = db.Column(db.Integer, db.ForeignKey('alergia.id_alergia'), primary_key = True)

    def __repr__():
        return f"ItenAlergia('{self.id_item}', '{self.id_alergia}')"

class EmentaItem(db.Model):
    """docstring for EmentaItem"""
    id_item = db.Column(db.Integer, db.ForeignKey('item.id_item'), primary_key = True)
    id_ementa = db.Column(db.Integer, db.ForeignKey('ementa.id_ementa'), primary_key = True)

    def __repr__():
        return f"EmentaItem('{self.id_item}', '{self.id_ementa}')"
