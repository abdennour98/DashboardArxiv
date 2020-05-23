from flask import Flask,render_template,request
import plotly.graph_objs as go
import plotly
from collections import OrderedDict
from pandas import DataFrame
import requests
import xmltodict    
import pandas as pd
import numpy as np
from wordcloud import WordCloud,STOPWORDS
from matplotlib import pyplot as plt
import json
import os

#function that returns a list of the authors
def namess(dfa):
    names=[]
    for i in range (0,dfa.count()):
        if(type(dfa[i])==list):
            for j in range(0,len(dfa[i])):
                names.append(dfa[i][j]['name'])
        else:
            names.append(dfa[i]['name'])
    return names


#fuction that returns a dataframe of the top 10 authors
def top10auth(var):
    dca={}
    for k in var:
        dca[k]=var.count(k)
    d2a = OrderedDict(sorted(dca.items(), key=lambda t: t[1],reverse=True))
    outa = json.loads(json.dumps(d2a))
    dg=pd.DataFrame(outa.items(), columns=['Name', 'Number of articles'])
    dg.index = np.arange(1, len(dg)+1)
    return dg.loc[ 1 : 10 ,:]

#Dictionary of categories
DictofCat={'cs.AI': 'Artificial Intelligence',
 'cs.CL': 'Computation and Language',
 'cs.CC': 'Computational Complexity',
 'cs.CE': 'Computational Engineering-Science',
 'cs.CG': 'Computational Geometry',
 'cs.GT': 'Computer Science & Game Theory',
 'cs.CV': 'Computer Vision & Pattern Recognition',
 'cs.CY': 'Computers and Society',
 'cs.CR': 'Cryptography and Security',
 'cs.DS': 'Data Structures and Algorithms',
 'cs.DB': 'Databases ',
 'cs.DL': 'Digital Libraries ',
 'cs.DM': 'Discrete Mathematics ',
 'cs.DC': 'Distributed,Parallel & Cluster Computing',
 'cs.ET': 'Emerging Technologies ',
 'cs.FL': 'Formal Languages & Automata Theory',
 'cs.GL': 'General Literature',
 'cs.GR': 'Graphics',
 'cs.AR': 'Hardware Architecture',
 'cs.HC': 'Human-Computer Interaction',
 'cs.IR': 'Information Retrieval',
 'math.IT': 'Information Theory',
 'cs.LO': 'Logic in Computer Science',
 'stat.ML': 'Machine Learning',
 'cs.MS': 'Mathematical Software',
 'cs.MA': 'Multiagent Systems',
 'cs.MM': 'Multimedia',
 'cs.NI': 'Networking & Internet Architecture',
 'cs.NE': 'Neural & Evolutionary Computing',
 'math.NA': 'Numerical Analysis',
 'cs.OS': 'Operating Systems',
 'cs.OH': 'Other Computer Science',
 'cs.PF': 'Performance',
 'cs.PL': 'Programming Languages',
 'cs.RO': 'Robotics',
 'cs.SI': 'Social & Information Networks',
 'cs.SE': 'Software Engineering',
 'cs.SD': 'Sound',
 'cs.SC': 'Symbolic Computation',
 'eess.SY': 'Systems & Control',
 'econ.EM': 'Econometrics',
 'econ.GN': 'General Economics',
 'econ.TH': 'Theoretical Economics',
 'eess.AS': 'Audio & Speech Processing',
 'eess.IV': 'Image & Video Processing',
 'eess.SP': 'Signal Processing',
 'math.AG': 'Algebraic Geometry',
 'math.AT': 'Algebraic Topology',
 'math.AP': 'Analysis of PDEs',
 'math.CT': 'Category Theory',
 'math.CA': 'Classical Analysis & ODEs',
 'math.CO': 'Combinatorics',
 'math.AC': 'Commutative Algebra',
 'math.CV': 'Complex Variables',
 'math.DG': 'Differential Geometry',
 'math.DS': 'Dynamical Systems',
 'math.FA': 'Functional Analysis',
 'math.GM': 'General Mathematics',
 'math.GN': 'General Topology',
 'math.GT': 'Geometric Topology',
 'math.GR': 'Group Theory',
 'math.HO': 'History & Overview',
 'math.KT': 'K-Theory & Homology',
 'math.LO': 'Logic',
 'math-ph': 'Mathematical Physics',
 'math.MG': 'Metric Geometry',
 'math.NT': 'Number Theory',
 'math.OA': 'Operator Algebras',
 'math.OC': 'Optimization & Control',
 'math.PR': 'Probability',
 'math.QA': 'Quantum Algebra',
 'math.RT': 'Representation Theory',
 'math.RA': 'Rings & Algebras',
 'math.SP': 'Spectral Theory',
 'stat.TH': 'Statistics Theory',
 'math.SG': 'Symplectic Geometry',
 'astro-ph.GA': 'Astrophysics of Galaxies',
 'astro-ph.CO': 'Cosmology-Nongalactic Astrophysics',
 'astro-ph.EP': 'Earth & Planetary Astrophysics',
 'astro-ph.HE': 'High Energy Astrophysical Phenomena',
 'astro-ph.IM': 'Instrumentation for Astrophysics',
 'astro-ph.SR': 'Solar & Stellar Astrophysics',
 'cond-mat.dis-nn': 'Disordered Systems & Neural Networks',
 'cond-mat.mtrl-sci': 'Materials Science',
 'cond-mat.mes-hall': 'Mesoscale & Nanoscale Physics',
 'cond-mat.other': 'Other Condensed Matter',
 'cond-mat.quant-gas': 'Quantum Gases',
 'cond-mat.soft': 'Soft Condensed Matter',
 'cond-mat.stat-mech': 'Statistical Mechanics',
 'cond-mat.str-el': 'Strongly Correlated Electrons',
 'cond-mat.supr-con': 'Superconductivity',
 'gr-qc': 'General Relativity-Quantum Cosmology',
 'hep-ex': 'High Energy Physics-Experiment',
 'hep-lat': 'High Energy Physics-Lattice',
 'hep-ph': 'High Energy Physics-Phenomenology',
 'hep-th': 'High Energy Physics-Theory',
 'nlin.AO': 'Adaptation & Self-Organizing Systems',
 'nlin.CG': 'Cellular Automata & Lattice Gases',
 'nlin.CD': 'Chaotic Dynamics',
 'nlin.SI': 'Exactly Solvable-Integrable Systems',
 'nlin.PS': 'Pattern Formation & Solitons',
 'nucl-ex': 'Nuclear Experiment',
 'nucl-th': 'Nuclear Theory',
 'physics.acc-ph': 'Accelerator Physics',
 'physics.app-ph': 'Applied Physics',
 'physics.ao-ph': 'Atmospheric & Oceanic Physics',
 'physics.atm-clus': 'Atomic & Molecular Clusters',
 'physics.atom-ph': 'Atomic Physics ',
 'physics.bio-ph': 'Biological Physics ',
 'physics.chem-ph': 'Chemical Physics ',
 'physics.class-ph': 'Classical Physics ',
 'physics.comp-ph': 'Computational Physics ',
 'physics.data-an': 'Data Analysis-Statistics-Probability',
 'physics.flu-dyn': 'Fluid Dynamics',
 'physics.gen-ph': 'General Physics',
 'physics.geo-ph': 'Geophysics ',
 'physics.hist-ph': 'History & Philosophy of Physics',
 'physics.ins-det': 'Instrumentation & Detectors',
 'physics.med-ph': 'Medical Physics ',
 'physics.optics': 'Optics',
 'physics.soc-ph': 'Physics & Society',
 'physics.ed-ph': 'Physics Education',
 'physics.plasm-ph': 'Plasma Physics',
 'physics.pop-ph': 'Popular Physics',
 'physics.space-ph': 'Space Physics',
 'quant-ph': 'Quantum Physics',
 'q-bio.BM': 'Biomolecules',
 'q-bio.CB': 'Cell Behavior',
 'q-bio.GN': 'Genomics',
 'q-bio.MN': 'Molecular Networks',
 'q-bio.NC': 'Neurons and Cognition',
 'q-bio.OT': 'Other Quantitative Biology',
 'q-bio.PE': 'Populations and Evolution',
 'q-bio.QM': 'Quantitative Methods ',
 'q-bio.SC': 'Subcellular Processes ',
 'q-bio.TO': 'Tissues and Organs ',
 'q-fin.CP': 'Computational Finance ',
 'q-fin.EC': 'Economics ',
 'q-fin.GN': 'General Finance ',
 'q-fin.MF': 'Mathematical Finance ',
 'q-fin.PM': 'Portfolio Management ',
 'q-fin.PR': 'Pricing of Securities ',
 'q-fin.RM': 'Risk Management ',
 'q-fin.ST': 'Statistical Finance ',
 'q-fin.TR': 'Trading & Market Microstructure',
 'stat.AP': 'Applications ',
 'stat.CO': 'Computation ',
 'stat.ME': 'Methodology ',
 'stat.OT': 'Other Statistics ',
 'astro-ph': 'Astrophysics ',
 'cond-mat': 'Condensed Matter ',
 'nlin': 'Noear Sciences ',
 'physics': 'Physics '}

#Function that returns a list of categories 
def categories(dfc):
    catc=[]
    for i in range(0,len(dfc)):
        if type(dfc[i]) == list:
            for j in range(0,len(dfc[i])):
                if(dfc[i][j]['@term'] in DictofCat):
                    catc.append(DictofCat[dfc[i][j]['@term']])
        elif(dfc[i]['@term'] in DictofCat):
            catc.append(DictofCat[dfc[i]['@term']])
    return catc 




#Function that returns a dataframe of the top 10 categories
def top10cat(var):
    dca={}
    for k in var:
        dca[k]=var.count(k)
    d2a = OrderedDict(sorted(dca.items(), key=lambda t: t[1],reverse=True))
    outa = json.loads(json.dumps(d2a))
    dg=pd.DataFrame(outa.items(), columns=['Category', 'Nb of occurence'])
    dg.index = np.arange(1, len(dg)+1)
    return dg.loc[ 1 : 10 ,:]

#Fonction which returns
def wordcloud(dfs,dft):
    total12=''
    for i in dft:
        total12=total12+i
    for j in dfs:
        total12=total12+j
    cloud = WordCloud(background_color='white',
                  max_words=300,
                  stopwords=STOPWORDS,
                 relative_scaling=0.5,
                  width=1000,
                  height=600
                 ).generate(total12)
    plt.imshow(cloud)
    plt.axis('off')
    plt.savefig('static/wordcloud.png',bbox_inches='tight')



app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
@app.route('/send',methods=['GET','POST'])
def send():
    if request.method =='POST':
        age = request.form['age']
        #######################Extraction of Data###########################
        r20=""
        for i in age:
            if i == ' ':
                r20 = r20 +'%20'
            else:
                r20 = r20 + i 
        r = requests.get('http://export.arxiv.org/api/query?search_query=all:'+r20+'&start=0&max_results=1000')
        xml = r.text
        doc=xmltodict.parse(xml)
        data = pd.DataFrame(doc)
        ######################################################################
        df=pd.DataFrame(data['feed']['entry'])
        dfa=df['author']
        dfc=df['category']
        dfs=df['summary']
        dfs=df['summary']
        dft=df['title']
        #######################################################################
      
        #######    Treatment and display of published articles    #############
        df['published']=df['published'].str.replace('T',' ')
        df['published']=df['published'].str.replace('Z',' ')
        df["published"]=pd.to_datetime(df["published"])
        df['year'] = pd.DatetimeIndex(df['published']).year
        nbpub=df.groupby("year").size().to_list()
        yearofpub=df.groupby("year").size().index.to_list()
        dg=pd.DataFrame({'Year': yearofpub,'Number of publications':nbpub})
        data2=[
            go.Bar(
                x=dg['Year'],
                y=dg['Number of publications'],
                name="Published Artciles"

            )
        ]
        bar2= json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
        #######################################################################


        
        #######    Treatment and display of updated articles    #############        
        df['updated']=df['updated'].str.replace('T',' ')
        df['updated']=df['updated'].str.replace('Z',' ')
        df["updated"]=pd.to_datetime(df["updated"])
        df['yearu'] = pd.DatetimeIndex(df['updated']).year
        nbup=df.groupby("yearu").size().to_list()
        yearofup=df.groupby("yearu").size().index.to_list()
        dup=pd.DataFrame({'Year': yearofup,'Number of publications':nbup})
        data1=[
           go.Bar(
             x=dup['Year'], 
             y=dup['Number of publications'],
             name="Updated Artciles",
            )
        ]
        bar1= json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
        #######################################################################

        ##########         Display of top 10 authors                 ##########
        names=namess(dfa)
        topauth=top10auth(names)

        ##########         Display of top 10 categries               ##########
        catc=categories(dfc)
        topcat=top10cat(catc)
        cat=topcat['Category'].tolist()
        numb=topcat['Nb of occurence'].tolist()
        graph_values = [{
                    'labels': cat,
                    'values': numb,
                    'type': 'pie',
                    'insidetextfont': {'color': '#FFFFFF',
                                        'size': '14',
                                        },
                    'textfont': {'color': '#FFFFFF',
                                        'size': '14',
                                },
                    }]

        layout = {} 
        ##########           Display of the wordcloud                 ##########
        wordcloud(dfs,dft)

        return render_template('dash.html', plot1 = bar1,plot2=bar2,
                                tables=[topauth.to_html(classes='topauthors')],graph_values=graph_values, layout=layout)
    return render_template('home.html')



@app.route('/contact')
def contact():
    return render_template('contact.html')




@app.route('/about')
def about():
   return render_template('about.html')


if __name__ =='__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
