import sys
sys.path.append('../')
from pycore.tikzeng import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),

    # Define custom colors
    r"""
    \definecolor{ConvColor}{RGB}{255, 234, 193}
    \definecolor{BatchNormColor}{RGB}{191,242,154}
    \definecolor{PReLUColor}{RGB}{216,183,92}
    \definecolor{LSTMColor}{RGB}{222, 239, 245}
    \definecolor{FcColor}{RGB}{214, 193, 234}
    \definecolor{TanhColor}{RGB}{255, 229, 234}
    """,
    
    #input (image)
    to_input('../images/csv.png'),
    
    # LSTM Block
    r"""
    \pic[shift={(0,0,0)}] at (0,0) 
    {Box={
        name=lstm,
        caption=LSTM,
        fill=LSTMColor,
        height=25,
        width=5,
        depth=25
        }
    };
    """,
    
    # FC Layer
    to_Dense(name='fc', n_filer=1, offset="(2,0,0)", to="(lstm-east)", 
            height=20, width=3, depth=20, caption="FC"),
    
    # First Conv Block
    to_Conv1D(name='conv1', n_filer=128, s_filer=1000, offset="(2,0,0)", to="(fc-east)", 
              height=20, width=3, depth=20, caption="Conv1D 128"),
    to_BatchNorm(name='bn1', to="(conv1-east)", height=20, width=2, depth=20),
    to_PReLU(name='prelu1', to="(bn1-east)", height=20, width=2, depth=20),
    
    # Second Conv Block
    to_Conv1D(name='conv2', n_filer=64, s_filer=1000, offset="(2,0,0)", to="(prelu1-east)", 
              height=15, width=3, depth=15, caption="Conv1D 64"),
    to_BatchNorm(name='bn2', to="(conv2-east)", height=15, width=2, depth=15),
    to_PReLU(name='prelu2', to="(bn2-east)", height=15, width=2, depth=15),
    
    # Final Conv Block
    to_Conv1D(name='conv3', n_filer=1, s_filer=1000, offset="(2,0,0)", to="(prelu2-east)", 
              height=10, width=3, depth=10, caption="Conv1D 1"),
    
    # Tanh Activation Block
    r"""
    \pic[shift={(2,0,0)}] at (conv3-east) 
    {Box={
        name=tanh,
        caption=Tanh,
        fill=TanhColor,
        height=10,
        width=2,
        depth=10
        }
    };
    """,
    
    # Output label (placed after tanh is defined)
    r"""\node[anchor=west, xshift=0.5cm] at (tanh-east) {\large Generated Sequence};""",
    
    # Connections
    to_connection("lstm", "fc"),
    to_connection("fc", "conv1"),
    to_connection("prelu1", "conv2"),
    to_connection("prelu2", "conv3"),
    to_connection("conv3", "tanh"),
    
    # Legend
    r"""
    \node[anchor=south east, draw, rounded corners, fill=white, align=left, font=\small\sffamily, yshift=-1cm] at (current bounding box.south east) {
        \begin{tabular}{@{}l@{\hspace{5pt}}l@{}}
        \textcolor{LSTMColor}{\rule{12pt}{12pt}} & LSTM \\
        \textcolor{FcColor}{\rule{12pt}{12pt}} & FC Layer \\
        \textcolor{ConvColor}{\rule{12pt}{12pt}} & Conv1D Layer \\
        \textcolor{BatchNormColor}{\rule{12pt}{12pt}} & BatchNorm \\
        \textcolor{PReLUColor}{\rule{12pt}{12pt}} & PReLU Activation \\
        \textcolor{TanhColor}{\rule{12pt}{12pt}} & Tanh \\
        \end{tabular}
    };
    """,
    
    to_end() 
]

def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')

if __name__ == '__main__':
    main()