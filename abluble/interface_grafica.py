import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import time
from resenha import AvaliadorTexto
from artigo import AvaliadorArtigo
from tkinter import scrolledtext

class InterfaceGrafica(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Avaliador de Texto")
        self.geometry("1400x900")  # Ajustei o tamanho do aplicativo
        self.configure(bg="#F0F0F0")  # Cor de fundo

        # Mapeamento de nomes para tornar os critérios mais legíveis
        self.mapeamento_nomes = {
            'Formatacao': 'Formatação:',
            'Linhas': 'Linhas:',
            'Citacoes': 'Citações:',
            'Lingua_Portuguesa': 'Língua Portuguesa:',
            'Adequacao': 'Adequação:'
        }

        # Variável para armazenar o perfil selecionado
        self.var_perfil = tk.StringVar(self)
        self.var_perfil.set("Resenha")  # Perfil padrão

        # Seletor de perfil
        self.lbl_seletor_perfil = tk.Label(self, text="Selecione o Perfil:", bg="#F0F0F0", font=("Helvetica", 12))
        self.lbl_seletor_perfil.grid(row=0, column=0, pady=10, padx=(100, 0), sticky="e")  # Ajuste para alinhar à direita
        self.dropdown_perfil = ttk.Combobox(self, textvariable=self.var_perfil, values=["Resenha", "Artigo"],
                                           font=("Helvetica", 12), state="readonly")
        self.dropdown_perfil.grid(row=0, column=1, pady=10, padx=(0, 20), sticky="w")  # Ajuste para alinhar à esquerda

        # Botão para selecionar o arquivo
        self.btn_selecionar_arquivo = tk.Button(self, text="Selecionar Arquivo", command=self.selecionar_arquivo,
                                                font=("Helvetica", 12), bg="#4CAF50", fg="white")
        self.btn_selecionar_arquivo.grid(row=1, column=0, pady=5, padx=(500, 0), sticky="w")  # Ajuste na opção padx

        # Botão de iniciar
        self.btn_iniciar = tk.Button(self, text="Iniciar Avaliação", command=self.iniciar_avaliacao,
                                    font=("Helvetica", 12), bg="#008CBA", fg="white")
        self.btn_iniciar.grid(row=1, column=1, pady=5, padx=(0, 500), sticky="e")  # Ajuste na opção padx

        # Frame para detalhes da pontuação
        self.frame_detalhes_pontuacao = tk.Frame(self, bg="#F0F0F0")
        self.frame_detalhes_pontuacao.grid(row=3, column=0, columnspan=2, pady=10, padx=20)  # Ajuste na opção padx

        # Label para exibir a pontuação total
        self.lbl_pontuacao_total = tk.Label(self.frame_detalhes_pontuacao, text="Pontuação: N/A", bg="#F0F0F0",
                                            font=("Helvetica", 14, "bold"))
        self.lbl_pontuacao_total.grid(row=0, column=0, columnspan=2, pady=10)

        # Frame para exibir os critérios e pontuações
        self.frame_critérios = tk.Frame(self.frame_detalhes_pontuacao, bg="#F0F0F0")
        self.frame_critérios.grid(row=1, column=0, columnspan=2, pady=10, padx=(20, 20))  # Ajuste na opção padx

        # Frame retangular para justificativas
        self.frame_justificativas = tk.Frame(self.frame_detalhes_pontuacao, bg="white", width=200, height=140)
        self.frame_justificativas.grid(row=1, column=4, padx=(20, 20), pady=5, sticky="n")

        # Label para título do frame de justificativas
        lbl_titulo_justificativas = tk.Label(self.frame_justificativas, text="Pontuações Detalhadas", bg="white", font=("Helvetica", 12, "bold"))
        lbl_titulo_justificativas.pack(side="top", pady=5)

        # Texto para mostrar as justificativas
        txt_justificativas = tk.Text(self.frame_justificativas, wrap="word", height=15, width=50, bg="white", font=("Helvetica", 10))
        txt_justificativas.pack(side="top", pady=5)

        # Frame retangular para feedback
        self.frame_feedback = tk.Frame(self.frame_detalhes_pontuacao, bg="white", width=500, height=200)
        self.frame_feedback.grid(row=3, column=0, padx=(20, 20), pady=5, sticky="n")

        # Adicione um frame para o texto do aluno
        self.frame_texto_aluno = tk.Frame(self, bg="#F0F0F0")
        self.frame_texto_aluno.grid(row=1, column=3, columnspan=2, pady=10, padx=10)

        # Adicione um widget de texto com rolagem para o texto do aluno
        self.texto_aluno_widget = scrolledtext.ScrolledText(self.frame_texto_aluno, wrap=tk.WORD, font=("Helvetica", 12))
        self.texto_aluno_widget.pack(fill=tk.BOTH, expand=True)

        # Configurar o grid para que os elementos possam expandir para ocupar o espaço disponível
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
            self.grid_columnconfigure(0, weight=1)


    def limpar_feedback(self):
        # Destrói todos os widgets no frame de feedback
        for widget in self.frame_feedback.winfo_children():
            widget.destroy()        

    def selecionar_arquivo(self):
        caminho_arquivo = filedialog.askopenfilename(filetypes=[("Arquivos DOCX", "*.docx")])
        if caminho_arquivo:
            self.caminho_arquivo = caminho_arquivo
            self.lbl_pontuacao_total.config(text="Pontuação: N/A")
            self.atualizar_detalhes_critérios({})  # Limpar detalhes dos critérios

    def iniciar_avaliacao(self):
        if hasattr(self, 'caminho_arquivo') and self.caminho_arquivo:
            self.tempo_inicio = time.time()

            # Importa a classe apropriada com base no perfil
            if self.var_perfil.get() == "Resenha":
                self.avaliador = AvaliadorTexto(perfil="Resenha")
            elif self.var_perfil.get() == "Artigo":
                self.avaliador = AvaliadorArtigo(perfil="Artigo")

            self.avaliar_arquivo(self.caminho_arquivo)
        else:
            messagebox.showinfo("Aviso", "Selecione um arquivo antes de iniciar a avaliação.")

    def avaliar_arquivo(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                texto_aluno = arquivo.read()
        except UnicodeDecodeError:
            messagebox.showerror("Erro", "Não foi possível decodificar o conteúdo do arquivo. Por favor, escolha outro arquivo.")
            return

        pontuacoes_detalhadas = self.avaliador.avaliar_texto(caminho_arquivo)

        self.tempo_fim = time.time()
        tempo_decorrido = self.tempo_fim - self.tempo_inicio

        # Exibe os detalhes da pontuação total
        pontuacao_total = sum(pontuacao['pontuacao'] for pontuacao in pontuacoes_detalhadas.values())
        self.lbl_pontuacao_total.config(text=f"Pontuação: {pontuacao_total:.2f}")

        # Exibe os detalhes dos critérios
        self.atualizar_detalhes_critérios(pontuacoes_detalhadas)

        # Marca as palavras incorretas no texto do aluno
        palavras_incorretas = self.avaliador.ler_palavras_incorretas_do_arquivo()
        self.marcar_palavras_incorretas(texto_aluno, palavras_incorretas)

        # Exibe o texto do aluno na interface gráfica
        self.exibir_texto_aluno(texto_aluno)

    def marcar_palavras_incorretas(self, texto_aluno, palavras_incorretas):
        # Função para marcar as palavras incorretas no texto do aluno
        for palavra_incorreta in palavras_incorretas:
            palavra_original = palavra_incorreta['original']

            # Encontrar todas as ocorrências da palavra original no texto do aluno
            start_index = texto_aluno.find(palavra_original)
            while start_index != -1:
                end_index = start_index + len(palavra_original)

                # Marcar a palavra original no texto do aluno
                self.texto_aluno_widget.tag_add('incorreta', f'1.{start_index}', f'1.{end_index}')

                # Encontrar a próxima ocorrência da palavra original
                start_index = texto_aluno.find(palavra_original, end_index)

        # Aplicar a formatação aos intervalos marcados
        self.texto_aluno_widget.tag_config('incorreta', foreground='red', font=('Helvetica', 12, 'bold'))
        
    def exibir_texto_aluno(self, texto):
        # Limpar o widget de texto do aluno
        self.texto_aluno_widget.delete("1.0", tk.END)

        # Inserir o texto no widget de texto
        self.texto_aluno_widget.insert(tk.END, texto)   

    def atualizar_detalhes_critérios(self, pontuacoes_detalhadas):
        # Limpar widgets antigos no frame_critérios
        for widget in self.frame_critérios.winfo_children():
            widget.destroy()

        # Limpar o texto antigo nas justificativas
        txt_justificativas = self.frame_justificativas.winfo_children()[1]
        txt_justificativas.delete('1.0', tk.END)

        # Criar widgets para cada critério
        for i, (criterio, pontuacao) in enumerate(pontuacoes_detalhadas.items(), start=1):
            # Nome formatado do critério usando o mapeamento
            nome_formatado = self.mapeamento_nomes.get(criterio, criterio)

            # Label para o nome do critério
            lbl_criterio = tk.Label(self.frame_critérios, text=nome_formatado, bg="#F0F0F0", font=("Helvetica", 12, "bold"))
            lbl_criterio.grid(row=i, column=0, padx=(20, 0), pady=5, sticky="w")  # Ajuste para alinhar à esquerda

            # Label para a pontuação do critério
            lbl_pontuacao = tk.Label(self.frame_critérios, text=f" {pontuacao['pontuacao']:.2f}", bg="#F0F0F0",
                                    font=("Helvetica", 12))
            lbl_pontuacao.grid(row=i, column=1, padx=(0, 20), pady=5, sticky="e")  # Ajuste para alinhar à direita

            # Label para a justificativa do critério
            lbl_justificativa = tk.Label(self.frame_critérios, text=pontuacao['justificativa'], bg="#F0F0F0",
                                        font=("Helvetica", 10))
            lbl_justificativa.grid(row=i, column=2, padx=20, pady=5, sticky="w", columnspan=2)  # Ajuste para alinhar à esquerda
    

        # Adiciona detalhes de pontuação na área de justificativas
        pontuacao_total = sum(pontuacao['pontuacao'] for pontuacao in pontuacoes_detalhadas.values())
        lbl_pontuacao_total = tk.Label(self.frame_detalhes_pontuacao, text=f"Pontuação: {pontuacao_total:.2f}", bg="#F0F0F0",
                                    font=("Helvetica", 14, "bold"))
        lbl_pontuacao_total.grid(row=0, column=0, columnspan=2, pady=10)
        
        for widget in self.frame_feedback.winfo_children():
            widget.grid_forget()
       
        # Adiciona feedback
        if pontuacao_total > 0:
            feedback = self.obter_feedback(pontuacao_total)
            lbl_feedback = tk.Label(self.frame_feedback, text=f"Feedback: {feedback}",
                                    font=("Helvetica", 10), wraplength=400)
            lbl_feedback.grid(row=3, column=1, columnspan=4, pady=5)

    def obter_feedback(self, pontuacao):
        if pontuacao < 6.0:
            return "Aluno, infelizmente seu trabalho não atingiu nota suficiente. De acordo com os requisitos apresentados, são necessárias muitas melhorias. Verifique a grade de correção para entender as falhas."
        elif 6.0 <= pontuacao <= 7.9:
            return "Aluno, seu trabalho está bom, mas precisa de algumas melhorias em relação aos requisitos de avaliação. Verifique a grade de correção para entender o que precisa ser ajustado para obter uma nota melhor."
        elif 8.0 <= pontuacao <= 9.9:
            return "Aluno, ótimo trabalho! Ele preenche grande parte dos requisitos de avaliação com nota acima da média. Verifique a grade de correção para entender o que precisaria melhorar."
        elif pontuacao >= 10.0:
            return "Parabéns, Aluno, excelente trabalho, cumpre todos os requisitos de avaliação com nota máxima!"
        else:
            return "Feedback não disponível"

if __name__ == "__main__":
    app = InterfaceGrafica()
    app.mainloop()