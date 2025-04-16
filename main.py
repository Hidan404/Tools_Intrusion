import rich
from rich.console import Console
import rich.text
import info_coletor
import Scanner
import bruteforce_login
import http_cabecalho
import forca_bruta_diretorios


def menu():
    console = Console()
    console.print("[bold blue][*] Ferramentas de teste de Intrusão[/bold blue]")
    console.print("[bold green]1. Coletar informações de domínio[/bold green]")
    console.print("[bold green]2. Scanner de portas[/bold green]")
    console.print("[bold green]3. Brute force em diretórios[/bold green]")
    console.print("[bold green]4. Conferir cabeçalho HTTP[/bold green]")
    console.print("[bold green]5. Força bruta de Diretorios[/bold green]")
    console.print("[bold green]6. Sair[/bold green]")

    while True:
        
        try:
            texto = rich.text.Text("Escolha uma opção:")
            texto.stylize("bold magenta", 0, 20)
            opcao = int(console.input("[bold blue]Digite sua opção: [/bold blue]"))
            if opcao == 1:
                console.print("[bold green]Coletar informações de domínio selecionado.[/bold green]")
                dominio = info_coletor.entrada_dominio()
                info_coletor.coletar_informacoes_dominio(dominio)  # Substitua pelo domínio desejado
            elif opcao == 2:
                console.print("[bold green]Scanner de portas selecionado.[/bold green]")
                Scanner.main()
            elif opcao == 3:
                console.print("[bold green]Brute force em diretórios selecionado.[/bold green]")
                forca_bruta_diretorios.main()
            elif opcao == 4:
                console.print("[bold red]conferindo  http cabeçalho[/bold red]")
                http_cabecalho.mostraar_cabecalho("https://www.linkedin.com/feed/")
            elif opcao == 5:
                console.print("[bold green]Força bruta de Diretórios selecionado.[/bold green]")
                bruteforce_login.main()
            elif opcao == 6:
                console.print("[bold red]Saindo...[/bold red]")
                break
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