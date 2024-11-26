import flet as ft

def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER #真ん中に表示されるようにしている

    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    #ページにaddしていくのが基本
    page.add( 
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click), #マイナスボタンを表示し、マイナスクリックで1マイナスする処理
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click), #プラスボタンを表示し、プラスクリックで1プラスする処理
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

ft.app(main)
