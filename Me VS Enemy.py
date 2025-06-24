import pygame
import random
import math

# Inicializa o pygame
pygame.init()

# Configuração da tela
largura, altura = 700, 1400
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Me Vs Enemy")

# Cores
branco = (255, 255, 255)
cinza = (100, 100, 100)
vermelho = (255, 0, 0)
preto = (0, 0, 0)
verde = (0, 255, 0)

# Função para exibir a tela de início
def tela_inicio():
    try:
         imagem_inicio = pygame.image.load("Tela de início.jpg")
         imagem_inicio = pygame.transform.scale(imagem_inicio, (2000, 2000))
         imagem_inicio = pygame.transform.rotate(imagem_inicio, -90)
         tela.blit(imagem_inicio, (-700, -240))
         
         fonte = pygame.font.Font(None, 50)# fonte e tamanho do texti
         texto = fonte.render("Desenvolvedor: Yuri dos Santos Martins ", True, verde)
         texto = pygame.transform.rotate(texto, -90)#rotacai do texto
         text_rect = texto.get_rect(topleft=(650, 150))#posicai do trxti
         tela.blit(texto, text_rect)#desenha o texto na tela
         
         texto2 = fonte.render("Gráficos: Leticia dos Santos Martins", True, verde)# texto
         texto2 = pygame.transform.rotate(texto2, -90)#rotacai do texto
         text_rect = texto2.get_rect(topleft=(620, 150))#posicai do trxti
         tela.blit(texto2, text_rect)#desenha o texto na tela
         
         pygame.display.flip()
    		
    except:
        tela.fill(preto)
        font = pygame.font.SysFont("Arial", 50)
        texto = font.render("PRESSIONE QUALQUER TECLA", True, branco)
        texto = pygame.transform.rotate(texto, -90)
        tela.blit(texto, (largura // 2 - 200, altura // 2))
        pygame.display.flip()
        
    play = pygame.Rect(50, 1000, 200, 500)

    esperando = True
    while esperando:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if play.collidepoint(ev.pos):
                	esperando = False

tela_inicio()

# Classe do joystick
class Joystick:
    def __init__(self, x, y, raio_base, raio_alavanca):
        self.x = x
        self.y = y
        self.raio_base = raio_base
        self.raio_alavanca = raio_alavanca
        self.alavanca_x = x
        self.alavanca_y = y
        self.ativo = False

    def desenhar(self):
        pygame.draw.circle(tela, cinza, (self.x, self.y), self.raio_base)
        pygame.draw.circle(tela, branco, (int(self.alavanca_x), int(self.alavanca_y)), self.raio_alavanca)

    def atualizar(self, pos):
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        distancia = math.sqrt(dx**2 + dy**2)

        if distancia > self.raio_base:
            fator = self.raio_base / distancia
            dx *= fator
            dy *= fator

        self.alavanca_x = self.x + dx
        self.alavanca_y = self.y + dy

    def reset(self):
        self.alavanca_x = self.x
        self.alavanca_y = self.y

    def get_direcao(self):
        dx = self.alavanca_x - self.x
        dy = self.alavanca_y - self.y
        return dx / self.raio_base, dy / self.raio_base

# Classe do inimigo
class Zombie1:
    def __init__(self):
        self.inimigos = []
        self.tamanho = 50
        self.velocidade = 3
        self.vida = 50
        try:
            self.imagem = pygame.image.load("Zombie1_direita.jpg")
            self.imagem = pygame.transform.scale(self.imagem, (70, 70))
            self.imagem = pygame.transform.rotate(self.imagem, -90)
        except:
            self.imagem = None  

    def criar_inimigo(self):
        inimigo_x = random.randint(100, largura - self.tamanho - 100)
        inimigo_y = random.randint(100, altura - self.tamanho - 100)
        self.inimigos.append({"x": inimigo_x, "y": inimigo_y, "vida": self.vida})

    def desenhar_inimigos(self):
        for inimigo in self.inimigos:
            if self.imagem:
                tela.blit(self.imagem, (inimigo["x"] -73, inimigo["y"] -15))#posicao

        # Criando uma superfície para a barra de vida
            barra_verde = pygame.Surface((inimigo["vida"], 5))
            barra_verde.fill((0, 255, 0))  # Cor verde
            barra_verde = pygame.transform.rotate(barra_verde, -90) #rotacao
        # Desenhando a barra de vida acima do inimigo
            tela.blit(barra_verde, (inimigo["x"], inimigo["y"] - 10))

# Classe do jogador
class Robson:
    def __init__(self, inimigos):
        self.tamanho = 50
        self.x = largura // 2
        self.y = altura // 2
        self.velocidade = 5
        self.vida = 100
        self.raio_ataque = 100
        self.dano_segundo = 1
        self.ponto = 0
        self.inimigos = inimigos
        self.novamente = False
        try:
            self.imagem = pygame.image.load("Player Robson_direita.jpg")
            self.imagem = pygame.transform.scale(self.imagem, (70, 70))
            self.imagem = pygame.transform.rotate(self.imagem, -90)
            
        except:
            self.imagem = None  

    def desenhar(self):
        if self.imagem:
            tela.blit(self.imagem, (self.x, self.y))
            
            pygame.draw.circle(tela, (250, 0, 0), (self.x + 35, self.y + 35), self.raio_ataque, 3)

    def mover(self, dx, dy):
        self.x += dx * self.velocidade
        self.y += dy * self.velocidade
        
        self.x = max(0, min(self.x, largura - 70))
        self.y = max(0, min(self.y, altura - 70))

    def atacar(self):
        for inimigo in self.inimigos.inimigos:
            centro_jogador_x = self.x + 50  # Ajustando para o centro do sprite
            centro_jogador_y = self.y + 50
            centro_inimigo_x = inimigo["x"] + 50
            centro_inimigo_y = inimigo["y"] + 50

            distancia = math.sqrt((centro_jogador_x - centro_inimigo_x)**2 + (centro_jogador_y - centro_inimigo_y)**2)
        
            if distancia < self.raio_ataque:
                inimigo["vida"] -= self.dano_segundo
                if inimigo["vida"] <= 0:
                    self.inimigos.inimigos.remove(inimigo)
                    self.ponto += 1

    def verificar_colisao(self):
        for inimigo in self.inimigos.inimigos:
            distancia = math.sqrt((self.x - inimigo["x"])**2 + (self.y - inimigo["y"])**2)
            if distancia < 20:
                self.vida -= 2
                
    def status(self):
    		fonte = pygame.font.Font(None, 40)# fonte e tamanho do texti
    		texto = fonte.render(f"Vida: {self.vida}  Pontos: {self.ponto}", True, branco)# texto
    		texto = pygame.transform.rotate(texto, -90)#rotacai do texto
    		text_rect = texto.get_rect(topleft=(650, 10))#posicai do trxti
    		
    		tela.blit(texto, text_rect)#desenha o texto na tela
    		

    def reiniciar_jogo(self):
        self.x = largura // 2
        self.y = altura // 2
        self.vida = 100
        self.ponto = 0
        self.inimigos.inimigos.clear()  # Limpa todos os inimigos
        self.novamente = False
    

    def game_over(self):
    	if self.vida <= 0:
            return True
            				
#classe do chao
class Chao:
	imagem_chao1 = pygame.image.load("chao1.jpg")
	imagem_chao1 = pygame.transform.scale(imagem_chao1, (1600, 700))
	imagem_chao1 = pygame.transform.rotate(imagem_chao1, -90)
	def desenhar_chao1(self):
		tela.blit(self.imagem_chao1, (0, 0))

# Criando os objetos
zombie1 = Zombie1()
player = Robson(zombie1)
joystick = Joystick(150, 150, 80, 40)
chao = Chao()

# Loop principal do jogo
rodando = True
while rodando:
    	
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            rodando = False
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if math.sqrt((ev.pos[0] - joystick.x) ** 2 + (ev.pos[1] - joystick.y) ** 2) < joystick.raio_base:
                joystick.ativo = True
                joystick.atualizar(ev.pos)
        elif ev.type == pygame.MOUSEMOTION and joystick.ativo:
            joystick.atualizar(ev.pos)
        elif ev.type == pygame.MOUSEBUTTONUP:
            joystick.ativo = False
            joystick.reset()

    dx, dy = joystick.get_direcao()
    player.mover(dx, dy)

    player.atacar()

    if random.random() < 0.02:
        zombie1.criar_inimigo()

    for inimigo in zombie1.inimigos:
        dx = player.x - inimigo["x"]
        dy = player.y - inimigo["y"]
        distancia = math.sqrt(dx**2 + dy**2)
        if distancia > 0:
            inimigo["x"] += (dx / distancia) * zombie1.velocidade
            inimigo["y"] += (dy / distancia) * zombie1.velocidade

    player.verificar_colisao()
    
    tela.fill(preto)
    chao.desenhar_chao1()
    zombie1.desenhar_inimigos()
    player.desenhar()
    player.status()
    joystick.desenhar()
    pygame.display.flip()
    pygame.time.delay(25)
    
    player.game_over = player.vida <= 0
    
    #chama funcao game over
    if player.game_over:
        imagem_gameover = pygame.image.load("tela gameover.jpg")
        imagem_gameover = pygame.transform.scale(imagem_gameover, (2000, 2000))
        imagem_gameover = pygame.transform.rotate(imagem_gameover, -90)
        tela.blit(imagem_gameover, (-640, -250))
    
        fonte = pygame.font.Font(None, 40)  # fonte
        texto = fonte.render(f"Pontos conquistados: {player.ponto}", True, preto)
        texto = pygame.transform.rotate(texto, -90)
        text_rect = texto.get_rect(center=(330, 740))
        tela.blit(texto, text_rect)
        pygame.display.flip()

    # Botões
        sair = pygame.Rect(0, 550, 100, 350)
        jogar_novamente = pygame.Rect(100, 550, 100, 350)
    
        botoes = True
        while botoes:
            for ev in pygame.event.get():
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    if sair.collidepoint(ev.pos):
                        pygame.quit()
                        exit()
                    if jogar_novamente.collidepoint(ev.pos):
                        player.reiniciar_jogo()
                        botoes = False
        continue
    
    

pygame.quit()
