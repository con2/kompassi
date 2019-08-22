# Kompassi Event Management System – New UI

## Getting started

    git clone git@github.com:tracon/kompassi
    git clone git@github.com:tracon/kompassi2

    cd kompassi2
    docker-compose up
    open http://localhost:3000

## License

    The MIT License (MIT)

    Copyright © 2018 Santtu Pajukanta

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.

## TODO

### Table component

### Schema form

- [ ] form serialization to JSON
  - [ ] `onChange` or sth
- [ ] initial values

### Form editor

- [ ] get the talkation between front and back workative
- [ ] emtypesafen
- [ ] implement new field parameters dialog / edit field dialog

### `<Tabs>`

- [ ] evaluate `react-bootstrap` v1 beta as an alternative to `reactstrap`
- [ ] change from `<Tabs ns="foo">{{ foo: <div>Bar</div> }}</Tabs>` to `<Tabs><Tab key="foo" title={t('Foo')}>Bar</Tab></Tabs>`
