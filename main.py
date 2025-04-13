import rich
from rich.console import Console
import rich.text
import info_coletor
import Scanner
import bruteforce_login
import http_cabecalho


def menu():
    console = Console()
    console.print("[bold blue][*] Ferramentas de teste de Intrusão[/bold blue]")
    console.print("[bold green]1. Coletar informações de domínio[/bold green]")
    console.print("[bold green]2. Scanner de portas[/bold green]")
    console.print("[bold green]3. Brute force em diretórios[/bold green]")

    while True:
        
        try:
            texto = rich.text.Text("Escolha uma opção:")
            texto.stylize("bold magenta", 0, 20)
            opcao = int(console.input("[bold blue]Digite sua opção: [/bold blue]"))
            if opcao == 1:
                console.print("[bold green]Coletar informações de domínio selecionado.[/bold green]")
                info_coletor.coletar_informacoes_dominio("https://www.linkedin.com/feed/")  # Substitua pelo domínio desejado
            elif opcao == 2:
                console.print("[bold green]Scanner de portas selecionado.[/bold green]")
                Scanner.Scanner_portas("13.107.42.14", [80, 443])  
            elif opcao == 3:
                console.print("[bold green]Brute force em diretórios selecionado.[/bold green]")
                bruteforce_login.bruteforce_login("https://www.linkedin.com/feed/", "usuario", "senha")  
            elif opcao == 4:
                console.print("[bold red]conferindo  http cabeçalho[/bold red]")
                http_cabecalho.mostraar_cabecalho("https://www.linkedin.com/feed/")
            else:
                console.print("[bold red]Opção inválida. Tente novamente.[/bold red]")
                continue
            break
        except KeyboardInterrupt:
            console.print("[bold red]Operação cancelada pelo usuário.[/bold red]")
            break
        except EOFError:
            console.print("[bold red]Entrada inválida. Tente novamente.[/bold red]")
            continue
        except TypeError:
            console.print("[bold red]Entrada inválida. Tente novamente.[/bold red]")
            continue
        except NameError:
            console.print("[bold red]Entrada inválida. Tente novamente.[/bold red]")
            continue
        except SyntaxError:
            console.print("[bold red]Entrada inválida. Tente novamente.[/bold red]")
            continue
        except ValueError:
            console.print("[bold red]Entrada inválida. Digite um número.[/bold red]")
            continue
    return opcao


if __name__ == "__main__":
    menu()