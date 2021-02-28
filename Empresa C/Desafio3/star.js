function avaliacao(nota){
    var completas = Number.parseInt(nota)
    var resto = nota-completas
    let estrelas = []
    for( p in [...Array(completas).keys()]){
        estrelas[p] = "star"
    }
    if(resto>0.5 && resto<0.99){
        estrelas.push('star_half')
    }
    while(estrelas.length<5){
        estrelas.push('star_border')
    }
    console.log(estrelas)
}

avaliacao(5)
avaliacao(0)
avaliacao(3.7)
avaliacao(3.2)
