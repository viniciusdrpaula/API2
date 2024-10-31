from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.turma import TurmaNaoEncontrada, listar_turmas, turma_por_id, adicionar_turma, atualizar_turma, excluir_turma

turma_blueprint = Blueprint('turma', __name__)

# ROTA PRINCIPAL PARA TURMAS
@turma_blueprint.route('/turma', methods=["GET"])
def rotas_turma():
    return 'Rotas para gerenciar turmas'

# ROTA PARA LISTAR TODAS AS TURMAS
@turma_blueprint.route('/turma', methods=['GET'])
def listar_todas_turmas():
    turmas = listar_turmas()
    return render_template("turma/turmas.html", turmas=turmas)

# ROTA PARA OBTER UMA TURMA ESPECÍFICA POR ID
@turma_blueprint.route('/turma/<int:id_turma>', methods=['GET'])
def detalhes_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma/turma_detalhes.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

# ROTA PARA EXIBIR O FORMULÁRIO DE CRIAÇÃO DE UMA NOVA TURMA
@turma_blueprint.route('/turma/adicionar', methods=['GET'])
def formulario_criar_turma():
    return render_template('turma/criar_turma.html')

# ROTA PARA CRIAR UMA NOVA TURMA
@turma_blueprint.route('/turma', methods=['POST'])
def cadastrar_turma():
    descricao = request.form.get('descricao')  # Usando get para evitar KeyError
    professor_id = request.form.get('professor_id')
    ativo = request.form.get('ativo') == 'on'
    turma_nova = {
        'descricao': descricao,
        'professor_id': professor_id,
        'ativo': ativo
    }
    adicionar_turma(turma_nova)
    return redirect(url_for('turmas.listar_todas_turmas'))

# ROTA PARA EXIBIR O FORMULÁRIO PARA EDITAR UMA TURMA
@turma_blueprint.route('/turma/<int:id_turma>/editar', methods=['GET'])
def formulario_editar_turma(id_turma):
    try:
        turma = turma_por_id(id_turma)
        return render_template('turma/turma_editar.html', turma=turma)
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

# ROTA PARA EDITAR UMA TURMA
@turma_blueprint.route('/turma/<int:id_turma>', methods=['POST'])
def atualizar_turma_info(id_turma):
    try:
        dados_atualizados = {
            'descricao': request.form.get('descricao'),
            'professor_id': request.form.get('professor_id'),
            'ativo': request.form.get('ativo') == 'on'
        }
        atualizar_turma(id_turma, dados_atualizados)
        return redirect(url_for('turmas.detalhes_turma', id_turma=id_turma))
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404

# ROTA PARA DELETAR UMA TURMA
@turma_blueprint.route('/turma/delete/<int:id_turma>', methods=['POST'])
def remover_turma(id_turma):
    try:
        excluir_turma(id_turma)
        return redirect(url_for('turmas.listar_todas_turmas'))
    except TurmaNaoEncontrada:
        return jsonify({'mensagem': 'Turma não encontrada'}), 404
