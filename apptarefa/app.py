import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

# Função para exibir informações sobre o aplicativo
def exibir_sobre():
    messagebox.showinfo("Sobre", "Meu App de Tarefas\nVersão 1.0\nDesenvolvido com Tkinter.")

# Função para limpar todas as tarefas
def limpar_tarefas():
    for tarefa in canvas_interior.winfo_children():
        tarefa.destroy()
    atualizar_contagem_tarefas()

# Função para sair do aplicativo
def sair_app():
    janela.quit()

# Criando a janela principal
janela = tk.Tk()
janela.title("Meu App de Tarefas")  # Define o título da janela
janela.configure(bg="#F0F0F0")      # Define a cor de fundo da janela
janela.geometry("500x600")          # Define o tamanho da janela

frame_em_edicao = None  # Variável global para armazenar o frame da tarefa em edição

# Função para adicionar uma tarefa
def adicionar_tarefa():
    global frame_em_edicao

    tarefa = entrada_tarefa.get().strip()  # Obtém o texto da entrada e remove espaços extras
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)  # Atualiza a tarefa existente
            frame_em_edicao = None
        else:
            adicionar_item_tarefa(tarefa)  # Adiciona nova tarefa
            entrada_tarefa.delete(0, tk.END)  # Limpa o campo de entrada
            atualizar_contagem_tarefas()  # Atualiza a contagem de tarefas
    else:
        messagebox.showwarning("Entrada inválida", "Por favor insira uma tarefa")

# Função para adicionar um item de tarefa à lista
def adicionar_item_tarefa(tarefa):
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd=1, relief=tk.SOLID)  # Cria um frame para a tarefa

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Garamond", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10)  # Adiciona o rótulo da tarefa ao frame

    botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l), bg="white", relief=tk.FLAT)
    botao_editar.pack(side=tk.RIGHT, padx=5)  # Adiciona o botão de editar ao frame

    botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda f=frame_tarefa: deletar_tarefa(f), bg="white", relief=tk.FLAT)
    botao_deletar.pack(side=tk.RIGHT, padx=5)  # Adiciona o botão de deletar ao frame

    frame_tarefa.pack(fill=tk.X, padx=5, pady=5)  # Adiciona o frame da tarefa ao canvas

    checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
    checkbutton.pack(side=tk.RIGHT, padx=5)  # Adiciona um checkbutton para marcar a tarefa como concluída

    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Atualiza a área de rolagem do canvas

# Função para preparar a edição de uma tarefa
def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_em_edicao
    frame_em_edicao = frame_tarefa
    entrada_tarefa.delete(0, tk.END)  # Limpa o campo de entrada
    entrada_tarefa.insert(0, label_tarefa.cget("text"))  # Insere o texto da tarefa no campo de entrada

# Função para atualizar uma tarefa existente
def atualizar_tarefa(nova_tarefa):
    global frame_em_edicao
    for widget in frame_em_edicao.winfo_children():
        if isinstance(widget, tk.Label):
            widget.config(text=nova_tarefa)  # Atualiza o texto do rótulo com a nova tarefa

# Função para deletar uma tarefa
def deletar_tarefa(frame_tarefa):
    frame_tarefa.destroy()  # Remove o frame da tarefa
    canvas_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Atualiza a área de rolagem do canvas
    atualizar_contagem_tarefas()  # Atualiza a contagem de tarefas

# Função para alternar o sublinhado do texto da tarefa
def alternar_sublinhado(label):
    fonte_atual = label.cget("font")
    if "overstrike" in fonte_atual:
        nova_fonte = fonte_atual.replace(" overstrike", "")
    else:
        nova_fonte = fonte_atual + " overstrike"
    label.config(font=nova_fonte)  # Atualiza a fonte do texto para incluir ou remover o sublinhado

# Função para contar o número de tarefas
def contar_tarefas():
    return len(canvas_interior.winfo_children())  # Retorna o número de widgets filhos (tarefas) no canvas_interior

# Função para atualizar o rótulo com a contagem de tarefas
def atualizar_contagem_tarefas():
    total_tarefas = contar_tarefas()  # Obtém o número total de tarefas
    rotulo_contagem.config(text=f"Total de Tarefas: {total_tarefas}")  # Atualiza o texto do rótulo com o total de tarefas

# Carregando os ícones
icon_editar = PhotoImage(file="edit.png").subsample(3, 3)
icon_deletar = PhotoImage(file="delete.png").subsample(3, 3)

# Configurando a fonte do cabeçalho
fonte_cabecalho = font.Font(family="Garamond", size=24, weight="bold")
rotulo_cabecalho = tk.Label(janela, text="Meu App de Tarefas", font=fonte_cabecalho, bg="#F0F0F0", fg="#333")
rotulo_cabecalho.pack(pady=20)  # Adiciona o rótulo do cabeçalho à janela

# Frame para a entrada de tarefas e botão de adicionar
frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

entrada_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="grey", width=30)
entrada_tarefa.pack(side=tk.LEFT, padx=10)

botao_adicionar = tk.Button(frame, command=adicionar_tarefa, text="Adicionar tarefa", bg="#4CAF50", fg="white", height=1, width=15, font=("Roboto", 11), relief=tk.FLAT)
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Criando um frame para a lista de tarefas com rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame_lista_tarefas, orient="vertical", command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Rótulo que mostra o total de tarefas
rotulo_contagem = tk.Label(janela, text="Total de Tarefas: 0", font=("Garamond", 14), bg="#F0F0F0", fg="#333")
rotulo_contagem.pack(pady=10)

# Criar o menu
menu_bar = tk.Menu(janela)
janela.config(menu=menu_bar)

menu_ajuda = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)
menu_ajuda.add_command(label="Sobre", command=exibir_sobre)

menu_edicao = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edição", menu=menu_edicao)
menu_edicao.add_command(label="Limpar Tarefas", command=limpar_tarefas)

menu_bar.add_command(label="Sair", command=sair_app)

janela.mainloop()  # Inicia o loop principal da interface gráfica

'''tkinter, ttk, font, messagebox, PhotoImage: Essas são as ferramentas importadas do Tkinter
responsáveis por criar a interface gráfica, trabalhar com fontes, 
mostrar mensagens de alerta, e carregar imagens.
'''
