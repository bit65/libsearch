# QUICK INSTALL

git submodule init
git submodule update

make -C ./ext/dexinfo/
pip install -e .

# RUN EXAMPLE

./examples/searcher.py