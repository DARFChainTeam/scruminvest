# popuvyper

Populus + vyper docker

attaches your_contracts_workdir may be (.) to container


sudo docker build -t popuvyper  https://github.com/stanta/popuvyper.git


use:
cd your_dir_with_smart_contracts

docker  run -it --mount type=bind,source="$(pwd)"/,target=/code  popuvyper:latest 

in docker type:
mc

or overway run as usual an get any over docker's candies!

enjoy! 

PS  Don't forget add to populus project.json:
{
    "version": "8",
    "compilation": {
        "contracts_source_dirs": ["./contracts"],
        "import_remappings": [],
        "backend": {
            "class": "populus.compilation.backends.VyperBackend"
        }
    }
}
