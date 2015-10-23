## Scan

Trans .md to .html

## Installition

    python bootstrap-buildout.py
    cd bin
    ./buildout
    
## Usage
    from zerg import document
    
    document = DocumentFpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.md')
    document.execute(Handler.SetAuthor('Mohanson'))
    document.execute(Handler.SetTitle())
    document.execute(Handler.SetDirectory())
    document.execute(Handler.DrawCode())
    print(document.soup)
    document.generate_fpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.html')
