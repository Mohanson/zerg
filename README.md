## Scan

trans .md to .html

## Installition

    python bootstrap-buildout.py
    cd bin
    ./buildout
    
## Usage

    cd bin
    zerg /home/user/README.md --author=Mohanson
    
## Or Use by Source Code

    from zerg.mark import DocumentFpath, Handler
    
    document = DocumentFpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.md')
    document.execute(Handler.SetAuthor('Mohanson'))
    document.execute(Handler.SetTitle())
    document.execute(Handler.SetDirectory())
    document.execute(Handler.DrawCode())
    print(document.soup)
    document.generate_fpath(r'C:\Users\Mohanson\PycharmProjects\zerg\README.html')
    
## How Connect me
    
    mailto: mohanson@outlook.com
    
