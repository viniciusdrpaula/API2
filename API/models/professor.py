from config import db

class Professor(db.Model):
    __tablename__ = 'professores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    
    turmas = db.relationship('Turma', back_populates='professor')

    def __init__(self, nome, idade=None, materia=None, observacoes=None):
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

class ProfessorNaoEncontrado(Exception):
    pass

def professor_por_id(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    return {
        'id': professor.id,
        'nome': professor.nome,
        'idade': professor.idade,
        'materia': professor.materia,
        'observacoes': professor.observacoes,
        'turmas': [{'id': turma.id, 'descricao': turma.descricao} for turma in professor.turmas]
    }

def listar_professores():
    professores = Professor.query.all()
    return [{
        'id': professor.id,
        'nome': professor.nome,
        'idade': professor.idade,
        'materia': professor.materia,
        'observacoes': professor.observacoes
    } for professor in professores]

def adicionar_professor(dados_professor):
    novo_professor = Professor(
        nome=dados_professor['nome'],
        idade=dados_professor.get('idade'),
        materia=dados_professor.get('materia'),
        observacoes=dados_professor.get('observacoes')
    )
    db.session.add(novo_professor)
    db.session.commit()

def atualizar_professor(id_professor, novos_dados):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    professor.nome = novos_dados.get('nome', professor.nome)
    professor.idade = novos_dados.get('idade', professor.idade)
    professor.materia = novos_dados.get('materia', professor.materia)
    professor.observacoes = novos_dados.get('observacoes', professor.observacoes)
    db.session.commit()

def excluir_professor(id_professor):
    professor = Professor.query.get(id_professor)
    if not professor:
        raise ProfessorNaoEncontrado
    db.session.delete(professor)
    db.session.commit()
