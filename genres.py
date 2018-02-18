from random import shuffle


def _random_iter(iterable):
    indices = list(range(len(iterable)))
    shuffle(indices)
    for i in indices:
        yield iterable[i]


class PlaylistNotFoundError(RuntimeError):
    """An error to be raised when a playlist for a genre wasn't found."""

    def __init__(self, genre):
        super().__init__('Playlist for {genre} could not be found!')


class Playlist:

    def __init__(self, p_id, name=None, url=None, image_url=None):
        if not p_id:
            self.found = False
        else:
            self.id = p_id
            self.name = name
            self.url = url
            self.image_url = image_url
            self.found = True

    @property
    def context_uri(self):
        return f'spotify:user:thesoundsofspotify:playlist:{self.id}'

    @classmethod
    def from_genre(cls, sp, genre):
        result = sp.search(
            f'The Sound of {genre.title()}', limit=1, type='playlist')
        items = result.get('playlists', {}).get('items')
        if not items:
            raise PlaylistNotFoundError(genre)
        pl = cls.from_item(items[0])
        pl.genre = genre
        return pl

    @classmethod
    def from_item(cls, item):
        p_id = item.get('id')
        try:
            pl_attributes = {
                'name': item['name'],
                'url': item['external_urls']['spotify'],
                'image_url': item['images'][0]['url'],
            }
        except (KeyError, AttributeError, IndexError):
            pl_attributes = {}
        return cls(p_id, **pl_attributes)

    @classmethod
    def fetch_random(cls, sp, count=3):
        choices = []
        random_iter = _random_iter(GENRES)
        for genre in random_iter:
            try:
                choices.append(Playlist.from_genre(sp, genre))
            except PlaylistNotFoundError:
                pass

            if len(choices) == count:
                return choices

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def __str__(self):
        return self.__repr__()


def play(sp, playlist, **kwargs):
    sp.start_playback(context_uri=playlist.context_uri, **kwargs)
    return {
        'replies':[{
            'type': 'text',
            'content': f"Playing '{playlist.url}'. Enjoy!",
        }],
        'conversation': {
          'memory': {'currently_playing': playlist.id}
        },
    }


GENRES = [
    '21st century classical',
    'a cappella',
    'abstract',
    'abstract beats',
    'abstract hip hop',
    'abstract idm',
    'abstractro',
    'accordeon',
    'accordion',
    'acid house',
    'acid jazz',
    'acid techno',
    'acousmatic',
    'acoustic blues',
    'acoustic pop',
    'adult standards',
    'african gospel',
    'african percussion',
    'african rock',
    'afrikaans',
    'afrobeat',
    'afrobeats',
    'aggrotech',
    'albanian pop',
    'album rock',
    'albuquerque indie',
    'alt-indie rock',
    'alternative americana',
    'alternative ccm',
    'alternative country',
    'alternative dance',
    'alternative emo',
    'alternative hardcore',
    'alternative hip hop',
    'alternative metal',
    'alternative metalcore',
    'alternative pop',
    'alternative pop rock',
    'alternative r&b',
    'alternative rock',
    'alternative roots rock',
    'ambeat',
    'ambient',
    'ambient dub techno',
    'ambient fusion',
    'ambient idm',
    'ambient psychill',
    'anarcho-punk',
    'andean',
    'anime',
    'anime cv',
    'anime score',
    'anthem emo',
    'anthem worship',
    'anti-folk',
    'antiviral pop',
    'appalachian folk',
    'arab folk',
    'arab pop',
    'arabesk',
    'argentine indie',
    'argentine reggae',
    'argentine rock',
    'armenian folk',
    'art pop',
    'art rock',
    'athens indie',
    'atmospheric black metal',
    'atmospheric post rock',
    'atmospheric post-metal',
    'aussietronica',
    'austindie',
    'australian alternative rock',
    'australian country',
    'australian dance',
    'australian hip hop',
    'australian indie',
    'australian pop',
    'austrian hip hop',
    'austropop',
    'avant-garde',
    'avant-garde jazz',
    'avantgarde metal',
    'axe',
    'azonto',
    'azontobeats',
    'bachata',
    'baile funk',
    'balearic',
    'balkan brass',
    'ballroom',
    'banda',
    'bangla',
    'barbershop',
    'barnemusikk',
    'barnmusik',
    'baroque',
    'baroque ensemble',
    'basque rock',
    'bass music',
    'bass trap',
    'bass trip',
    'bassline',
    'bay area hip hop',
    'bay area indie',
    'beach music',
    'beatdown',
    'beats',
    'bebop',
    'belgian indie',
    'belgian rock',
    'belly dance',
    'belorush',
    'bemani',
    'benga',
    'bhangra',
    'big band',
    'big beat',
    'big room',
    'black death',
    'black metal',
    'black sludge',
    'black thrash',
    'blackgaze',
    'blaskapelle',
    'bluegrass',
    'blues',
    'blues-rock',
    'blues-rock guitar',
    'bmore',
    'bolero',
    'boogaloo',
    'boogie-woogie',
    'bossa nova',
    'bossa nova jazz',
    'boston rock',
    'bounce',
    'bouncy house',
    'bow pop',
    'boy band',
    'brass band',
    'brass ensemble',
    'brazilian ccm',
    'brazilian composition',
    'brazilian electronica',
    'brazilian gospel',
    'brazilian hip hop',
    'brazilian indie',
    'brazilian punk',
    'breakbeat',
    'breakcore',
    'breaks',
    'brega',
    'breton folk',
    'brill building pop',
    'british alternative rock',
    'british blues',
    'british brass band',
    'british dance band',
    'british folk',
    'british indie rock',
    'british invasion',
    'britpop',
    'broadway',
    'broken beat',
    'brooklyn indie',
    'brostep',
    'brutal death metal',
    'brutal deathcore',
    'bubble trance',
    'bubblegum dance',
    'bubblegum pop',
    'bulgarian folk',
    'bulgarian rock',
    'byzantine',
    'c-pop',
    'c64',
    'c86',
    'cabaret',
    'cajun',
    'calypso',
    'canadian country',
    'canadian hip hop',
    'canadian indie',
    'canadian metal',
    'canadian pop',
    'candy pop',
    'cantautor',
    'cante flamenco',
    'canterbury scene',
    'cantopop',
    'canzone napoletana',
    'capoeira',
    'carnatic',
    'carnaval',
    'catalan folk',
    'catstep',
    'caucasian folk',
    'ccm',
    'ceilidh',
    'cello',
    'celtic',
    'celtic christmas',
    'celtic punk',
    'celtic rock',
    'central asian folk',
    'chalga',
    'chamame',
    'chamber choir',
    'chamber pop',
    'chamber psych',
    'channel pop',
    'chanson',
    'chanson quebecois',
    'chaotic black metal',
    'chaotic hardcore',
    'charred death',
    'chicago blues',
    'chicago house',
    'chicago indie',
    'chicago soul',
    'chicano rap',
    "children's christmas",
    "children's music",
    'chilean rock',
    'chill groove',
    'chill lounge',
    'chill-out trance',
    'chillhop',
    'chillstep',
    'chillwave',
    'chinese experimental',
    'chinese indie rock',
    'chinese opera',
    'chinese traditional',
    'chip hop',
    'chiptune',
    'choral',
    'choro',
    'christelijk',
    'christian alternative rock',
    'christian christmas',
    'christian dance',
    'christian hardcore',
    'christian hip hop',
    'christian metal',
    'christian music',
    'christian punk',
    'christian relaxative',
    'christian rock',
    'christian uplift',
    'christmas',
    'christmas product',
    'cinematic dubstep',
    'clarinet',
    'classic afrobeat',
    'classic belgian pop',
    'classic chinese pop',
    'classic colombian pop',
    'classic czech pop',
    'classic danish pop',
    'classic dutch pop',
    'classic eurovision',
    'classic finnish pop',
    'classic finnish rock',
    'classic french pop',
    'classic funk rock',
    'classic garage rock',
    'classic icelandic pop',
    'classic italian pop',
    'classic norwegian pop',
    'classic peruvian pop',
    'classic polish pop',
    'classic psychedelic rock',
    'classic rock',
    'classic russian pop',
    'classic russian rock',
    'classic schlager',
    'classic soundtrack',
    'classic swedish pop',
    'classic turkish pop',
    'classic venezuelan pop',
    'classical',
    'classical cello',
    'classical christmas',
    'classical era',
    'classical flute',
    'classical guitar',
    'classical organ',
    'classical percussion',
    'classical performance',
    'classical piano',
    'classify',
    'college a cappella',
    'college marching band',
    'colombian rock',
    'columbus ohio indie',
    'comedy',
    'comedy rock',
    'comic',
    'commons',
    'complextro',
    'compositional ambient',
    'concert band',
    'consort',
    'contemporary classical',
    'contemporary country',
    'contemporary folk',
    'contemporary jazz',
    'contemporary post-bop',
    'cool jazz',
    'cornetas y tambores',
    'corrosion',
    'corsican folk',
    'country',
    'country blues',
    'country christmas',
    'country dawn',
    'country gospel',
    'country road',
    'country rock',
    'coupe decale',
    'coverchill',
    'covertrance',
    'cowboy western',
    'crack rock steady',
    'croatian pop',
    'crossover prog',
    'crossover thrash',
    'crunk',
    'crust punk',
    'cryptic black metal',
    'cuban rumba',
    'cubaton',
    'cumbia',
    'cumbia funk',
    'cumbia pop',
    'cumbia sonidera',
    'cumbia villera',
    'cyber metal',
    'czech folk',
    'czech hip hop',
    'czech rock',
    'dallas indie',
    'dance pop',
    'dance rock',
    'dance-punk',
    'dancehall',
    'dangdut',
    'danish hip hop',
    'danish indie',
    'danish jazz',
    'danish pop',
    'danish pop rock',
    'dansband',
    'danseband',
    'dansktop',
    'danspunk',
    'dark ambient',
    'dark black metal',
    'dark cabaret',
    'dark electro-industrial',
    'dark hardcore',
    'dark jazz',
    'dark minimal techno',
    'dark progressive house',
    'dark psytrance',
    'dark wave',
    'darkstep',
    'death core',
    'death metal',
    'deathgrind',
    'deep acoustic pop',
    'deep adult standards',
    'deep ambient',
    'deep australian indie',
    'deep big room',
    'deep brazilian pop',
    'deep breakcore',
    'deep canadian indie',
    'deep ccm',
    'deep chill',
    'deep chill-out',
    'deep chiptune',
    'deep christian rock',
    'deep classic garage rock',
    'deep comedy',
    'deep contemporary country',
    'deep cumbia sonidera',
    'deep dance pop',
    'deep danish pop',
    'deep darkpsy',
    'deep deep house',
    'deep deep tech house',
    'deep delta blues',
    'deep disco',
    'deep disco house',
    'deep discofox',
    'deep downtempo fusion',
    'deep dub techno',
    'deep dutch hip hop',
    'deep east coast hip hop',
    'deep euro house',
    'deep eurodance',
    'deep filthstep',
    'deep flow',
    'deep folk metal',
    'deep free jazz',
    'deep freestyle',
    'deep full on',
    'deep funk',
    'deep funk carioca',
    'deep funk house',
    'deep g funk',
    'deep german hip hop',
    'deep german indie',
    'deep german jazz',
    'deep german pop rock',
    'deep german punk',
    'deep gothic post-punk',
    'deep groove house',
    'deep happy hardcore',
    'deep hardcore',
    'deep hardcore punk',
    'deep hardstyle',
    'deep house',
    'deep indian pop',
    'deep indie pop',
    'deep indie r&b',
    'deep indie rock',
    'deep indie singer-songwriter',
    'deep italo disco',
    'deep jazz fusion',
    'deep jazz guitar',
    'deep jazz piano',
    'deep latin alternative',
    'deep latin christian',
    'deep latin hip hop',
    'deep latin jazz',
    'deep liquid',
    'deep liquid bass',
    'deep melodic death metal',
    'deep melodic euro house',
    'deep melodic hard rock',
    'deep melodic metalcore',
    'deep minimal techno',
    'deep motown',
    'deep neo-synthpop',
    'deep neofolk',
    'deep new americana',
    'deep new wave',
    'deep nordic folk',
    'deep norteno',
    'deep northern soul',
    'deep nz indie',
    'deep orgcore',
    'deep pop edm',
    'deep pop emo',
    'deep pop punk',
    'deep pop r&b',
    'deep power-pop punk',
    'deep progressive house',
    'deep progressive trance',
    'deep psychobilly',
    'deep psytrance',
    'deep punk rock',
    'deep ragga',
    'deep rai',
    'deep regional mexican',
    'deep smooth jazz',
    'deep soft rock',
    'deep soul house',
    'deep soundtrack',
    'deep southern soul',
    'deep southern trap',
    'deep space rock',
    'deep sunset lounge',
    'deep surf music',
    'deep swedish hip hop',
    'deep swedish indie pop',
    'deep swedish rock',
    'deep symphonic black metal',
    'deep taiwanese pop',
    'deep talent show',
    'deep tech house',
    'deep texas country',
    'deep thrash metal',
    'deep trap',
    'deep tropical house',
    'deep turkish pop',
    'deep underground hip hop',
    'deep uplifting trance',
    'deep vocal house',
    'deep vocal jazz',
    'delta blues',
    'demoscene',
    'denver indie',
    'depressive black metal',
    'desert blues',
    'desi',
    'desi hip hop',
    'destroy techno',
    'detroit hip hop',
    'detroit techno',
    'didgeridoo',
    'digital hardcore',
    'dirty south rap',
    'dirty texas rap',
    'disco',
    'disco house',
    'disco polo',
    'discofox',
    'disney',
    'dixieland',
    'djent',
    'dominican pop',
    'doo-wop',
    'doom metal',
    'doomcore',
    'doujin',
    'downtempo',
    'downtempo fusion',
    'drama',
    'dream pop',
    'dreamo',
    'drift',
    'drill',
    'drill and bass',
    'drone',
    'drone folk',
    'drone metal',
    'drone psych',
    'drum and bass',
    'drumfunk',
    'dub',
    'dub techno',
    'dubstep',
    'dubstep product',
    'dubsteppe',
    'duranguense',
    'dutch hip hop',
    'dutch house',
    'dutch pop',
    'dutch rock',
    'dwn trap',
    'e6fi',
    'early modern classical',
    'early music',
    'early music ensemble',
    'east coast hip hop',
    'easy listening',
    'ebm',
    'ectofolk',
    'ecuadoria',
    'edm',
    'electric blues',
    'electro',
    'electro bailando',
    'electro dub',
    'electro house',
    'electro jazz',
    'electro latino',
    'electro swing',
    'electro trash',
    'electro-industrial',
    'electroacoustic improvisation',
    'electroclash',
    'electrofox',
    'electronic',
    'electronic trap',
    'electronica',
    'electronicore',
    'electropowerpop',
    'electropunk',
    'emo',
    'emo punk',
    'enka',
    'entehno',
    'environmental',
    'epicore',
    'escape room',
    'estonian pop',
    'ethereal gothic',
    'ethereal wave',
    'etherpop',
    'ethiopian pop',
    'eurodance',
    'europop',
    'euroska',
    'eurovision',
    'exotica',
    'experimental',
    'experimental dubstep',
    'experimental psych',
    'experimental rock',
    'fado',
    'fake',
    'fallen angel',
    'faroese pop',
    'fast melodic punk',
    'fidget house',
    'filmi',
    'filter house',
    'filthstep',
    'fingerstyle',
    'finnish dance pop',
    'finnish hardcore',
    'finnish hip hop',
    'finnish indie',
    'finnish jazz',
    'finnish metal',
    'finnish pop',
    'flamenco',
    'flick hop',
    'float house',
    'fluxwork',
    'focus',
    'folk',
    'folk christmas',
    'folk metal',
    'folk punk',
    'folk rock',
    'folk-pop',
    'folklore argentino',
    'folkmusik',
    'football',
    'footwork',
    'forro',
    'fourth world',
    'francoton',
    'freak folk',
    'freakbeat',
    'free improvisation',
    'free jazz',
    'freestyle',
    'french folk',
    'french folk pop',
    'french hip hop',
    'french indie pop',
    'french indietronica',
    'french movie tunes',
    'french pop',
    'french punk',
    'french reggae',
    'french rock',
    'full on',
    'funeral doom',
    'funk',
    'funk carioca',
    'funk metal',
    'funk rock',
    'funky breaks',
    'funky tech house',
    'fussball',
    'future ambient',
    'future funk',
    'future garage',
    'futurepop',
    'g funk',
    'gabba',
    'galego',
    'gamecore',
    'gamelan',
    'gangster rap',
    'garage pop',
    'garage psych',
    'garage punk',
    'garage punk blues',
    'garage rock',
    'gauze pop',
    'gbvfi',
    'geek folk',
    'geek rock',
    'german ccm',
    'german hip hop',
    'german indie',
    'german metal',
    'german oi',
    'german pop',
    'german pop rock',
    'german punk',
    'german show tunes',
    'german street punk',
    'german techno',
    'ghazal',
    'ghettotech',
    'ghoststep',
    'girl group',
    'glam metal',
    'glam rock',
    'glitch',
    'glitch beats',
    'glitch hop',
    'glitter trance',
    'go-go',
    'goa trance',
    'goregrind',
    'gospel',
    'gospel blues',
    'gospel reggae',
    'gothic alternative',
    'gothic americana',
    'gothic doom',
    'gothic metal',
    'gothic post-punk',
    'gothic rock',
    'gothic symphonic metal',
    'grave wave',
    'greek hip hop',
    'greek house',
    'greek indie',
    'grim death metal',
    'grime',
    'grindcore',
    'grisly death metal',
    'groove metal',
    'groove room',
    'grunge',
    'grunge pop',
    'grupera',
    'guidance',
    'guitar case',
    'gypsy jazz',
    'halloween',
    'hands up',
    'happy hardcore',
    'hard alternative',
    'hard bop',
    'hard glam',
    'hard house',
    'hard minimal techno',
    'hard rock',
    'hard stoner rock',
    'hardcore',
    'hardcore breaks',
    'hardcore hip hop',
    'hardcore punk',
    'hardcore techno',
    'hardstyle',
    'harmonica blues',
    'harp',
    'harpsichord',
    'hatecore',
    'hauntology',
    'hawaiian',
    'healing',
    'heavy alternative',
    'heavy christmas',
    'heavy gothic rock',
    'hebrew pop',
    'highlife',
    'hindustani classical',
    'hip hop',
    'hip hop quebecois',
    'hip hop tuga',
    'hip house',
    'hip pop',
    'hiplife',
    'hoerspiel',
    'hollywood',
    'horror punk',
    'horrorcore',
    'house',
    'hungarian hip hop',
    'hungarian pop',
    'hungarian rock',
    'hyphy',
    'icelandic hip hop',
    'icelandic pop',
    'icelandic rock',
    'idol',
    'indian classical',
    'indian folk',
    'indian pop',
    'indian rock',
    'indie anthem-folk',
    'indie christmas',
    'indie dream pop',
    'indie electro-pop',
    'indie emo',
    'indie emo rock',
    'indie folk',
    'indie fuzzpop',
    'indie garage rock',
    'indie jazz',
    'indie pop',
    'indie pop rock',
    'indie poptimism',
    'indie psych-pop',
    'indie psych-rock',
    'indie punk',
    'indie r&b',
    'indie rock',
    'indie rockism',
    'indie shoegaze',
    'indie singer-songwriter',
    'indiecoustica',
    'indietronica',
    'indonesian indie',
    'indonesian pop',
    'indorock',
    'industrial',
    'industrial metal',
    'industrial rock',
    'instrumental post rock',
    'intelligent dance music',
    'irish country',
    'irish folk',
    'irish indie',
    'irish rock',
    'iskelma',
    'islamic recitation',
    'israeli pop',
    'israeli rock',
    'italian arena pop',
    'italian disco',
    'italian folk',
    'italian hip hop',
    'italian indie pop',
    'italian jazz',
    'italian metal',
    'italian pop',
    'italian pop rock',
    'italian progressive rock',
    'italian punk',
    'italo beats',
    'italo dance',
    'j-ambient',
    'j-core',
    'j-dance',
    'j-idol',
    'j-indie',
    'j-metal',
    'j-pop',
    'j-poppunk',
    'j-poprock',
    'j-punk',
    'j-rap',
    'j-reggae',
    'j-rock',
    'jam band',
    'jangle pop',
    'jangle rock',
    'japanese city pop',
    'japanese jazztronica',
    'japanese psychedelic',
    'japanese r&b',
    'japanese traditional',
    'japanoise',
    'jazz',
    'jazz bass',
    'jazz blues',
    'jazz brass',
    'jazz christmas',
    'jazz composition',
    'jazz funk',
    'jazz fusion',
    'jazz metal',
    'jazz orchestra',
    'jazz trio',
    'jig and reel',
    'judaica',
    'jug band',
    'jump blues',
    'jump up',
    'jumpstyle',
    'jungle',
    'k-hop',
    'k-indie',
    'k-pop',
    'k-rock',
    'kabarett',
    'karneval',
    'kayokyoku',
    'kc indie',
    'kids dance party',
    'kindermusik',
    'kirtan',
    'kiwi rock',
    'kizomba',
    'klapa',
    'klezmer',
    'kompa',
    'korean pop',
    'kraut rock',
    'kuduro',
    'kurdish folk',
    'kwaito',
    'kwaito house',
    'la indie',
    'laboratorio',
    'laiko',
    'latin',
    'latin alternative',
    'latin arena pop',
    'latin christian',
    'latin christmas',
    'latin electronica',
    'latin hip hop',
    'latin jazz',
    'latin metal',
    'latin pop',
    'latvian pop',
    'lds',
    'leeds indie',
    'levenslied',
    'library music',
    'liedermacher',
    'lift kit',
    'light music',
    'lilith',
    'liquid funk',
    'lithumania',
    'liturgical',
    'lo star',
    'lo-fi',
    'louisiana blues',
    'louisville indie',
    'lounge',
    'lounge house',
    'louvor',
    'lovers rock',
    'lowercase',
    'luk thung',
    'madchester',
    'maghreb',
    'magyar',
    'makina',
    'makossa',
    'malagasy folk',
    'malaysian pop',
    'mallet',
    'mambo',
    'mande pop',
    'mandible',
    'mandopop',
    'manele',
    'mantra',
    'marching band',
    'mariachi',
    'martial industrial',
    'mashup',
    'math pop',
    'math rock',
    'mathcore',
    'mbalax',
    'medieval',
    'medieval folk',
    'medieval rock',
    'meditation',
    'melancholia',
    'melbourne bounce',
    'mellow gold',
    'melodic death metal',
    'melodic hard rock',
    'melodic hardcore',
    'melodic metalcore',
    'melodic power metal',
    'melodic progressive metal',
    'melodipop',
    'memphis blues',
    'memphis hip hop',
    'memphis soul',
    'merengue',
    'merengue urbano',
    'merseybeat',
    'metal',
    'metal guitar',
    'metalcore',
    'metropopolis',
    'mexican indie',
    'mexican rock-and-roll',
    'mexican son',
    'mexican traditional',
    'miami bass',
    'michigan indie',
    'microhouse',
    'microtonal',
    'military band',
    'minimal',
    'minimal dub',
    'minimal dubstep',
    'minimal melodic techno',
    'minimal tech house',
    'minimal techno',
    'minimal wave',
    'mizrahi',
    'mod revival',
    'modern blues',
    'modern country rock',
    'modern downshift',
    'modern free jazz',
    'modern performance',
    'modern rock',
    'modern southern rock',
    'modern uplift',
    'monastic',
    'moombahton',
    'morna',
    'motivation',
    'motown',
    'movie tunes',
    'mpb',
    'musica nativista',
    'musica para ninos',
    'musica per bambini',
    'musiikkia lapsille',
    'musique concrete',
    'musique pour enfants',
    'muziek voor kinderen',
    'nasheed',
    'nashville sound',
    'native american',
    'necrogrind',
    'neo classical metal',
    'neo honky tonk',
    'neo mellow',
    'neo metal',
    'neo soul',
    'neo soul-jazz',
    'neo-industrial rock',
    'neo-pagan',
    'neo-progressive',
    'neo-psychedelic',
    'neo-rockabilly',
    'neo-singer-songwriter',
    'neo-synthpop',
    'neo-trad metal',
    'neo-traditional country',
    'neoclassical',
    'neofolk',
    'nepali',
    'nerdcore',
    'neue deutsche harte',
    'neue deutsche welle',
    'neurofunk',
    'neurostep',
    'new age',
    'new age piano',
    'new americana',
    'new beat',
    'new jack smooth',
    'new jack swing',
    'new orleans blues',
    'new orleans jazz',
    'new rave',
    'new romantic',
    'new tribe',
    'new wave',
    'new wave pop',
    'new weird america',
    'ninja',
    'nintendocore',
    'nl folk',
    'no wave',
    'noise',
    'noise pop',
    'noise punk',
    'noise rock',
    'nordic folk',
    'nordic house',
    'norteno',
    'northern irish indie',
    'northern soul',
    'norwegian gospel',
    'norwegian hip hop',
    'norwegian indie',
    'norwegian jazz',
    'norwegian metal',
    'norwegian pop',
    'norwegian punk',
    'norwegian rock',
    'nu age',
    'nu disco',
    'nu electro',
    'nu gaze',
    'nu jazz',
    'nu metal',
    'nu skool breaks',
    'nu-cumbia',
    'nueva cancion',
    'nursery',
    'nwobhm',
    'nwothm',
    'nz indie',
    'oi',
    'ok indie',
    'old school hip hop',
    'old-time',
    'opera',
    'operatic pop',
    'opm',
    'oratory',
    'orchestral',
    'organic ambient',
    'orgcore',
    'orquesta tipica',
    'orquesta tropical',
    'oshare kei',
    'ostrock',
    'otacore',
    'outer hip hop',
    'outlaw country',
    'outsider',
    'outsider house',
    'p funk',
    'pagan black metal',
    'pagode',
    'pakistani pop',
    'panpipe',
    'permanent wave',
    'persian pop',
    'persian traditional',
    'perth indie',
    'peruvian rock',
    'piano blues',
    'piano rock',
    'piedmont blues',
    'pinoy alternative',
    'pipe band',
    'pixie',
    'poetry',
    'polish hip hop',
    'polish indie',
    'polish jazz',
    'polish pop',
    'polish punk',
    'polish reggae',
    'polka',
    'polynesian pop',
    'polyphony',
    'pop',
    'pop christmas',
    'pop emo',
    'pop flamenco',
    'pop house',
    'pop punk',
    'pop rap',
    'pop reggaeton',
    'pop rock',
    'popgaze',
    'porro',
    'portland indie',
    'portuguese pop',
    'portuguese rock',
    'post rock',
    'post-disco',
    'post-disco soul',
    'post-doom metal',
    'post-grunge',
    'post-hardcore',
    'post-metal',
    'post-post-hardcore',
    'post-punk',
    'post-screamo',
    'post-teen pop',
    'power blues-rock',
    'power electronics',
    'power metal',
    'power noise',
    'power pop',
    'power violence',
    'power-pop punk',
    'praise',
    'prank',
    'preverb',
    'progressive alternative',
    'progressive bluegrass',
    'progressive deathcore',
    'progressive electro house',
    'progressive house',
    'progressive metal',
    'progressive post-hardcore',
    'progressive psytrance',
    'progressive rock',
    'progressive trance',
    'progressive trance house',
    'progressive uplifting trance',
    'protopunk',
    'psych gaze',
    'psychedelic blues-rock',
    'psychedelic doom',
    'psychedelic rock',
    'psychedelic trance',
    'psychill',
    'psychobilly',
    'pub rock',
    'puerto rican rock',
    'punjabi',
    'punk',
    'punk blues',
    'punk christmas',
    'punk ska',
    'punta',
    'qawwali',
    'quebecois',
    'quiet storm',
    'r&b',
    'ragga jungle',
    'ragtime',
    'rai',
    'ranchera',
    'rap',
    'rap chileno',
    'rap metal',
    'rap metalcore',
    'rap rock',
    'raw black metal',
    're:techno',
    'reading',
    'rebetiko',
    'redneck',
    'reggae',
    'reggae fusion',
    'reggae rock',
    'reggaeton',
    'reggaeton flow',
    'regional mexican',
    'regional mexican pop',
    'relaxative',
    'remix',
    'renaissance',
    'retro electro',
    'retro metal',
    'rhythm and boogie',
    'riddim',
    'rio de la plata',
    'riot grrrl',
    'rock',
    'rock catala',
    'rock en espanol',
    'rock gaucho',
    'rock noise',
    'rock steady',
    'rock-and-roll',
    'rockabilly',
    'romanian pop',
    'romanian rock',
    'romantic era',
    'romantico',
    'roots reggae',
    'roots rock',
    'rosary',
    'rumba',
    'russelater',
    'russian alternative',
    'russian folk',
    'russian hip hop',
    'russian pop',
    'russian punk',
    'russian rock',
    'russiavision',
    'rva indie',
    'salsa',
    'salsa international',
    'samba',
    'samba-enredo',
    'saxophone',
    'schlager',
    'schranz',
    'scorecore',
    'scottish rock',
    'scratch',
    'screamo',
    'screamo punk',
    'screamocore',
    'seattle indie',
    'sega',
    'semba',
    'serialism',
    'sertanejo',
    'sertanejo tradicional',
    'sertanejo universitario',
    'shanty',
    'sheffield indie',
    'shibuya-kei',
    'shimmer pop',
    'shimmer psych',
    'shiver pop',
    'shoegaze',
    'show tunes',
    'singaporean pop',
    'singer-songwriter',
    'sinhala',
    'ska',
    'ska punk',
    'ska revival',
    'skate punk',
    'skiffle',
    'skinhead oi',
    'skinhead reggae',
    'skweee',
    'sky room',
    'slam death metal',
    'slash punk',
    'slavic metal',
    'slc indie',
    'sleaze rock',
    'sleep',
    'slovak hip hop',
    'slovak pop',
    'slovenian rock',
    'slow core',
    'slow game',
    'sludge metal',
    'smooth jazz',
    'smooth urban r&b',
    'soca',
    'soda pop',
    'soft rock',
    'solipsynthm',
    'song poem',
    'soukous',
    'soul',
    'soul blues',
    'soul christmas',
    'soul flow',
    'soul jazz',
    'sound art',
    'soundtrack',
    'south african jazz',
    'southern gospel',
    'southern hip hop',
    'southern rock',
    'southern soul',
    'southern soul blues',
    'space rock',
    'spanish classical',
    'spanish folk',
    'spanish hip hop',
    'spanish indie pop',
    'spanish indie rock',
    'spanish invasion',
    'spanish new wave',
    'spanish noise pop',
    'spanish pop',
    'spanish pop rock',
    'spanish punk',
    'spanish reggae',
    'spanish rock',
    'speed garage',
    'speed metal',
    'speedcore',
    'spoken word',
    'spytrack',
    'steampunk',
    'steelpan',
    'stl indie',
    'stomp and flutter',
    'stomp and holler',
    'stomp and whittle',
    'stomp pop',
    'stoner metal',
    'stoner rock',
    'straight edge',
    'street punk',
    'stride',
    'string band',
    'string folk',
    'string quartet',
    'strut',
    'substep',
    'sunset lounge',
    'suomi rock',
    'surf music',
    'swamp blues',
    'swamp pop',
    'swedish alternative rock',
    'swedish eurodance',
    'swedish folk pop',
    'swedish hard rock',
    'swedish hip hop',
    'swedish idol pop',
    'swedish indie pop',
    'swedish indie rock',
    'swedish jazz',
    'swedish jazz orkester',
    'swedish metal',
    'swedish pop',
    'swedish pop punk',
    'swedish prog',
    'swedish punk',
    'swedish reggae',
    'swedish synthpop',
    'swing',
    'swiss hip hop',
    'swiss rock',
    'symphonic black metal',
    'symphonic metal',
    'symphonic rock',
    'synthpop',
    'taiwanese pop',
    'talent show',
    'tango',
    'tanzlmusi',
    'tech house',
    'technical brutal death metal',
    'technical death metal',
    'techno',
    'teen pop',
    'tejano',
    'tekno',
    'terrorcore',
    'texas blues',
    'texas country',
    'thai idol',
    'thai indie',
    'thai pop',
    'theme',
    'thrash core',
    'thrash metal',
    'thrash-groove metal',
    'throat singing',
    'tibetan',
    'tico',
    'timba',
    'tin pan alley',
    'tone',
    'tracestep',
    'traditional blues',
    'traditional british folk',
    'traditional country',
    'traditional folk',
    'traditional funk',
    'traditional reggae',
    "traditional rock 'n roll",
    'traditional rockabilly',
    'traditional scottish folk',
    'traditional ska',
    'traditional soul',
    'traditional swing',
    'trance',
    'trap francais',
    'trap latino',
    'trap music',
    'trash rock',
    'triangle indie',
    'tribal house',
    'tribute',
    'trip hop',
    'tropical',
    'tropical house',
    'trova',
    'turbo folk',
    'turkish alternative',
    'turkish classical',
    'turkish folk',
    'turkish hip hop',
    'turkish jazz',
    'turkish pop',
    'turkish rock',
    'turntablism',
    'twee indie pop',
    'twee pop',
    'twin cities indie',
    'tzadik',
    'ugandan pop',
    'uk drill',
    'uk dub',
    'uk funky',
    'uk garage',
    'uk hip hop',
    'uk post-punk',
    'ukrainian rock',
    'ukulele',
    'unblack metal',
    'underground hip hop',
    'underground latin hip hop',
    'underground pop rap',
    'underground power pop',
    'underground rap',
    'uplifting trance',
    'urban contemporary',
    'usbm',
    'vallenato',
    'vancouver indie',
    'vapor house',
    'vapor pop',
    'vapor soul',
    'vapor twitch',
    'vaporwave',
    'vegan straight edge',
    'vegas indie',
    'velha guarda',
    'venezuelan rock',
    'video game music',
    'vienna indie',
    'vietnamese pop',
    'viking metal',
    'villancicos',
    'vintage chanson',
    'vintage country folk',
    'vintage french electronic',
    'vintage gospel',
    'vintage italian soundtrack',
    'vintage jazz',
    'vintage reggae',
    'vintage rockabilly',
    'vintage schlager',
    'vintage swedish pop',
    'vintage swing',
    'vintage swoon',
    'vintage tango',
    'vintage western',
    'violin',
    'viral pop',
    'visual kei',
    'vocal house',
    'vocal jazz',
    'vocaloid',
    'voidgaze',
    'volksmusik',
    'warm drone',
    'wave',
    'welsh rock',
    'west african jazz',
    'west coast rap',
    'west coast trap',
    'western swing',
    'wind ensemble',
    'witch house',
    'wonky',
    'workout',
    'world',
    'world chill',
    'world christmas',
    'world fusion',
    'world meditation',
    'world worship',
    'worship',
    'wrestling',
    'wrock',
    'ye ye',
    'yoik',
    'yugoslav rock',
    'zapstep',
    'zeuhl',
    'zillertal',
    'zim',
    'zolo',
    'zouglou',
    'zouk',
    'zouk riddim',
    'zydeco'
]