from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

# cria a conexao entre a API do banco de dados e o banco de dados fisico.
engine = create_engine('sqlite:///:memory:', echo=False)
Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)
	password = Column(String)

	def __init__(self, name, fullname, password):
		self.name = name
		self.fullname = fullname
		self.password = password

	def __repr__(self):
		return "<User('%s', '%s', '%s')>" % (self.name, self.fullname, self.password)

class Address(Base):
	__tablename__ = 'addresses'
	id = Column(Integer, primary_key=True)
	email_address = Column(String, nullable=False)
	# user_id relaciona as duas tabelas 
	# com o uso do objeto ForeignKey
	user_id = Column(Integer, ForeignKey('users.id'))

	# relationship e backref criam relacionamentos muitos-para-um e um-para-muitos respectivamente
	user = relationship("User", backref=backref('addresses', order_by=id))

	def __init__(self, email_address):
		self.email_address = email_address

	def __repr__(self):
		return "<Address('%s')>" % self.email_address	

# cria as tabelas que estao relacionadas na declaracao Base, usando o objeo engine criado.
Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

# cria usuario
fulano = User('fulano', 'Fulano da Silva', 'fulano123')
session.add(fulano)

usuario = session.query(User).filter_by(name='fulano').first()
print(usuario)

print('Usuario fulano == usuario?', fulano is usuario)

# cria varios usuarios com a utilizacao do metodo add_all
session.add_all([
	User('ciclano', 'Ciclano da Silva', 'ciclano123'),
	User('beltrano', 'Beltrano da Silva', 'beltrano123')])

fulano.password = 'fulano456'

print("Area da sessao com objetos atualizados:", session.dirty)

print("Area da sessao com objetos novos:", session.new)

# persiste os dados no banco de dados.
session.commit()

print("Agora fulano.id esta disponivel pois foi gerado pela engine do banco de dados SQLite. ID: %d" % (fulano.id))

# deletando usuario ciclano
session.query(User).filter_by(name='ciclano').delete()

# veja que o usuario nao consta nesse retorno
for u in session.query(User).all():
	print("Usuario/Nome:", u, u.name)

# caso a operacao precise ser desfeita, rollback
session.rollback()

# veja que o usuario ciclano agora esta
for u in session.query(User).all():
	print("Usuario/Nome:", u, u.name)

chico = User('chico', 'Francisco da Silva', 'chico123')
print ("Enderecos para chicho", chico.addresses)

# criando enderecos para o usuario chico
chico.addresses = [Address(email_address='chico123@gmail.com'),
					Address(email_address='franciscochico123@gmail.com')]

# adicionando chico e os enderecos de chico
session.add(chico)
session.commit()

# verificando o usuario chico
chico = session.query(User).filter_by(name='chico').one()
print(chico)

# vericando os enderecos do usuario chico
print(chico.addresses)


