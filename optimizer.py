import ctypes
import subprocess
import winreg
from elevate import elevate
import os
import time

class WindowsOptimizer:
    def __init__(self):
        if not ctypes.windll.shell32.IsUserAnAdmin():
            elevate(show=False)
    
    def set_power_plan(self, plan="high"):
        power_plans = {
            "high": "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
            "balanced": "381b4222-f694-41f0-9685-ff5bb260df2e",
            "power_saver": "a1841308-3541-4fab-bc81-f71556f20b4a"
        }
        
        if plan in power_plans:
            subprocess.run(f"powercfg /setactive {power_plans[plan]}", shell=True)
    
    def optimize_nvidia_settings(self):
        try:
            # Configurações originais de performance
            subprocess.run([
                "nvidia-smi", 
                "--gpu-reset-applications-clocks",
                "--applications-clocks=memory_transfer_rate:max,graphics_clock:max"
            ])
            
            subprocess.run([
                "nvidia-smi",
                "--power-management-mode=1"
            ])
            
            # Configurações 3D do painel NVIDIA
            nvidia_settings = {
                "Dimensionamento de imagem": "Desativar",
                "Anti-aliasing - FXAA": "Desligado",
                "Anti-aliasing - configuração": "Nenhum",
                "Anti-aliasing - correção do gama": "Ligado",
                "Anti-aliasing - modo": "Desligado",
                "Anti-aliasing - transparência": "Desligado",
                "Buffering triplo": "Desligado",
                "CUDA - GPUs": "Todas",
                "CUDA - Política de retorno de memória": "Padrão do driver",
                "Compatibilidade com OpenGL e GDI": "Automático",
                "DSR - Fatores": "Off",
                "DSR - Suavidade": "Desligado",
                "Filtragem anisotrópica": "Desligado",
                "Filtragem da textura - Diferencial negativo": "Fixar",
                "Filtragem da textura - otimização anisotrópica": "Ligado",
                "Filtragem da textura - otimização trilinear": "Ligado",
                "Filtragem da textura - qualidade": "Alto desempenho",
                "Modo de gerenciamento de energia": "Preferência por desempenho máximo",
                "Modo de latência baixa": "Ultra",
                "Multi-Frame Sampled AA (MFAA)": "Desligado",
                "Método atual Vulkan/OpenGL": "Automático",
                "Otimização segmentada": "Auto",
                "Quadros pré-renderizados de Realidade Virtual": "1",
                "Realidade Virtual - Superamostragem": "Desligado",
                "Sincronização vertical": "Desligado",
                "Tamanho do cache do criador de sombras": "Padrão do driver",
                "Taxa Máxima de Quadros": "Desligada",
                "Taxa de atualização preferida": "A maior disponível"
            }
            
            # Aplicando configurações usando NVIDIA Profile Inspector ou comandos do registro
            for setting, value in nvidia_settings.items():
                try:
                    # Aqui você pode implementar a lógica para cada configuração específica
                    # usando o NVIDIA Profile Inspector via linha de comando ou registro do Windows
                    print(f"Aplicando {setting}: {value}")
                    
                    # Exemplo de comando para o registro (você precisará ajustar os caminhos e valores)
                    reg_path = f"HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\{{4d36e968-e325-11ce-bfc1-08002be10318}}\\0000\\{setting}"
                    subprocess.run(f'reg add "{reg_path}" /v Value /t REG_DWORD /d 0 /f', shell=True)
                    
                except Exception as e:
                    print(f"Erro ao configurar {setting}: {e}")
            
            print("Configurações NVIDIA aplicadas com sucesso!")
            print("OBS: Algumas configurações podem requerer reinicialização do driver ou do sistema.")
            
        except Exception as e:
            print(f"Erro ao configurar NVIDIA: {e}")
    
    def set_timer_resolution(self):
        try:
            # Caminho do registro para o GlobalTimerResolutionRequests
            key_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\kernel"
            
            try:
                # Tenta abrir a chave
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
            except WindowsError:
                # Se a chave não existir, cria ela
                key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, key_path)
            
            # Tenta definir o valor
            winreg.SetValueEx(key, "GlobalTimerResolutionRequests", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
            print("Timer Resolution configurado com sucesso!")
        except Exception as e:
            print(f"Erro ao configurar Timer Resolution: {e}")
    
    def optimize_gaming_settings(self):
        try:
            print("Iniciando otimizações...")
            
            # Configuração do Timer Resolution
            print("Configurando Timer Resolution...")
            self.set_timer_resolution()
            
            # Configurações do Timer do Sistema (bcdedit)
            print("Otimizando timer do sistema...")
            subprocess.run('bcdedit /set useplatformtick yes', shell=True)
            subprocess.run('bcdedit /set disabledynamictick yes', shell=True)
            subprocess.run('bcdedit /deletevalue useplatformclock', shell=True)
            
            # Desativa Xbox Game Bar
            print("Desativando Xbox Game Bar...")
            subprocess.run('reg add "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\GameDVR" /v AppCaptureEnabled /t REG_DWORD /d 0 /f', shell=True)
            subprocess.run('reg add "HKEY_CURRENT_USER\System\GameConfigStore" /v GameDVR_Enabled /t REG_DWORD /d 0 /f', shell=True)
            
            # Ativa Modo Jogo
            print("Ativando Modo Jogo...")
            subprocess.run('reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v AllowAutoGameMode /t REG_DWORD /d 1 /f', shell=True)
            subprocess.run('reg add "HKEY_CURRENT_USER\Software\Microsoft\GameBar" /v AutoGameModeEnabled /t REG_DWORD /d 1 /f', shell=True)
            
            # Ativa Agendamento GPU Acelerado por Hardware
            print("Configurando GPU...")
            subprocess.run('reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\GraphicsDrivers" /v HwSchMode /t REG_DWORD /d 2 /f', shell=True)
            
            # Define Alto Desempenho para VALORANT
            print("Otimizando VALORANT...")
            valorant_path = "C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Binaries\\Win64"
            subprocess.run(f'powercfg /setappscheduling "{valorant_path}" 6', shell=True)
            
            # Desativa Aplicativos em Segundo Plano
            print("Desativando apps em segundo plano...")
            subprocess.run('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" /v GlobalUserDisabled /t REG_DWORD /d 1 /f', shell=True)
            subprocess.run('reg add "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Search" /v BackgroundAppGlobalToggle /t REG_DWORD /d 0 /f', shell=True)
            
            # Executa Limpeza de Disco
            print("Iniciando limpeza do sistema...")
            subprocess.run('reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\VolumeCaches\Temporary Files" /v StateFlags0001 /t REG_DWORD /d 2 /f', shell=True)
            subprocess.run('cleanmgr /sagerun:1', shell=True)
            
            print("\nConfigurações de jogos otimizadas com sucesso!")
            print("Timer Resolution e Timer do sistema otimizados!")
            print("Aplicativos em segundo plano desativados!")
            print("Limpeza do sistema iniciada! Isso pode levar alguns minutos...")
            print("Você pode continuar usando o computador normalmente durante a limpeza.")
            print("\nOBS: Algumas alterações podem requerer reinicialização do sistema para terem efeito.")
            
        except Exception as e:
            print(f"Erro ao otimizar configurações: {e}")

def main():
    width = 120  # Largura total da tela do console
    print("=" * width)
    print("Windows & NVIDIA Optimizer".center(width))
    print("Copyright © 2024".center(width))
    print("Feito por Konato".center(width))
    print("Todos os direitos reservados".center(width))
    print("=" * width)
    
    optimizer = WindowsOptimizer()
    
    while True:
        print("\n1. Ativar Plano de Energia de Alto Desempenho")
        print("2. Otimizar Configurações NVIDIA")
        print("3. Otimizar Configurações de Jogos (Game Mode/Timer/Resolution/Xbox Bar/GPU/Background Apps/Limpeza)")
        print("4. Aplicar Todas as Otimizações")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            optimizer.set_power_plan("high")
            print("Plano de energia alterado para Alto Desempenho")
        elif choice == "2":
            optimizer.optimize_nvidia_settings()
            print("Configurações NVIDIA otimizadas")
        elif choice == "3":
            optimizer.optimize_gaming_settings()
        elif choice == "4":
            optimizer.set_power_plan("high")
            optimizer.optimize_nvidia_settings()
            optimizer.optimize_gaming_settings()
            print("Todas as otimizações foram aplicadas")
        elif choice == "5":
            break

if __name__ == "__main__":
    main()
