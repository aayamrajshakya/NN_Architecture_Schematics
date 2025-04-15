import sys
sys.path.append('../')
from pycore.tikzeng import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),

    # Define custom colors first
    r"""
    \definecolor{ConvColor}{RGB}{255,234,193}  % Yellow-orange for Conv layers
    \definecolor{BatchNormColor}{RGB}{191,242,154}  % Light green for BatchNorm
    \definecolor{PReLUColor}{RGB}{216,183,92}  % Light red for PReLU
    \definecolor{DropoutColor}{RGB}{181,168,132}  % Gray for Dropout
    \definecolor{PoolColor}{RGB}{231,153,153}  % Gray for Dropout
    \definecolor{FcColor}{RGB}{214,193,234}  % Gray for Dropout

    """,
    
    #input (image)
    to_input('../images/snr_plot.png'),

    # Input (optional - remove if not needed)
    # to_input('input.png', to="(0,0,0)", width=2, height=2, name="input"),
    
    # First Conv Block - More vertical spacing
    to_Conv1D(name='conv1', n_filer=64, s_filer=256, offset="(0,0,0)", to="(0,0,0)", 
              height=30, width=3, depth=30, caption="Conv1D 64"),
    to_BatchNorm(name='bn1', to="(conv1-east)", height=30, width=2, depth=30),
    to_PReLU(name='prelu1', to="(bn1-east)", height=30, width=2, depth=30),
    to_Dropout(name='drop1', to="(prelu1-east)", height=30, width=2, depth=30),
    
    # Second Conv Block - Increased horizontal spacing
    to_Conv1D(name='conv2', n_filer=128, s_filer=128, offset="(3,0,0)", to="(drop1-east)", 
              height=25, width=3, depth=25, caption="Conv1D 128"),
    to_BatchNorm(name='bn2', to="(conv2-east)", height=25, width=2, depth=25),
    to_PReLU(name='prelu2', to="(bn2-east)", height=25, width=2, depth=25),
    to_Dropout(name='drop2', to="(prelu2-east)", height=25, width=2, depth=25),
    
    # Third Conv Block
    to_Conv1D(name='conv3', n_filer=256, s_filer=64, offset="(3,0,0)", to="(drop2-east)", 
              height=20, width=3, depth=20, caption="Conv1D 256"),
    to_BatchNorm(name='bn3', to="(conv3-east)", height=20, width=2, depth=20),
    to_PReLU(name='prelu3', to="(bn3-east)", height=20, width=2, depth=20),
    to_Dropout(name='drop3', to="(prelu3-east)", height=20, width=2, depth=20),
    
    # Fourth Conv Block
    to_Conv1D(name='conv4', n_filer=512, s_filer=32, offset="(3,0,0)", to="(drop3-east)", 
              height=15, width=3, depth=15, caption="Conv1D 512"),
    to_BatchNorm(name='bn4', to="(conv4-east)", height=15, width=2, depth=15),
    to_PReLU(name='prelu4', to="(bn4-east)", height=15, width=2, depth=15),
    to_Dropout(name='drop4', to="(prelu4-east)", height=15, width=2, depth=15),
    
    # Global Average Pooling - More vertical space before final layer
    to_GlobalAvgPool1D(name='gap', offset="(2,0,0)", to="(drop4-east)", 
                      height=10, width=4, depth=10, caption="Adaptive Average Pooling"),
    
    # Final Dense Layer - Larger spacing
    to_Dense(name='output', n_filer=1, offset="(2,0,0)", to="(gap-east)", 
            height=8, width=3, depth=8, caption="Output"),
    
    # Output label
    r"""\node[anchor=west, xshift=0.5cm] at (output-east) {\large Real/Fake Decision};""",    

    to_connection("drop1", "conv2"),
    to_connection("drop2", "conv3"),
    to_connection("drop3", "conv4"),
    to_connection("drop4", "gap"),
    to_connection("gap", "output"),

    # Add legend in bottom right (after architecture)
    r"""
    \node[anchor=south east, draw, rounded corners, fill=white, align=left, font=\small\sffamily, yshift=-1cm] at (current bounding box.south east) {
        \begin{tabular}{@{}l@{\hspace{5pt}}l@{}}
        \textcolor{ConvColor}{\rule{12pt}{12pt}} & Conv1D Layer \\
        \textcolor{BatchNormColor}{\rule{12pt}{12pt}} & BatchNorm \\
        \textcolor{PReLUColor}{\rule{12pt}{12pt}} & PReLU Activation \\
        \textcolor{DropoutColor}{\rule{12pt}{12pt}} & Dropout \\
        \textcolor{PoolColor}{\rule{12pt}{12pt}} & GlobalAvgPool \\
        \textcolor{FcColor}{\rule{12pt}{12pt}} & Output Layer \\
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
