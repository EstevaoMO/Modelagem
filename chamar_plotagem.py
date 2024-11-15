import webbrowser
import http.server
import socketserver

PORT = 8000

# Cria o servidor
Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print(f"Servindo em http://localhost:{PORT}")

# Abre o navegador padrão
webbrowser.open(f'http://localhost:{PORT}/index.html')

# Inicia o servidor
httpd.serve_forever()