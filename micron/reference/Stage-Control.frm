VERSION 5.00
Object = "{648A5603-2C6E-101B-82B6-000000000014}#1.1#0"; "MSCOMM32.OCX"
Begin VB.Form StageControl 
   Caption         =   "Stage Control 4.3"
   ClientHeight    =   9660
   ClientLeft      =   420
   ClientTop       =   705
   ClientWidth     =   8805
   LinkTopic       =   "Form1"
   ScaleHeight     =   9660
   ScaleWidth      =   8805
   StartUpPosition =   3  'Windows Default
   Begin VB.CommandButton SaveVariable 
      Caption         =   "Save Current Variable"
      Height          =   495
      Left            =   7320
      TabIndex        =   241
      Top             =   3720
      Width           =   1095
   End
   Begin VB.Frame Frame1 
      Caption         =   "Frame1"
      Height          =   255
      Left            =   6240
      TabIndex        =   222
      Top             =   6720
      Visible         =   0   'False
      Width           =   735
      Begin VB.CommandButton Command10 
         Caption         =   "Command10"
         Height          =   375
         Left            =   4080
         TabIndex        =   236
         Top             =   240
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.TextBox Text7 
         Height          =   375
         Left            =   3840
         TabIndex        =   235
         Text            =   "Text7"
         Top             =   960
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.TextBox Text8 
         Height          =   375
         Left            =   3840
         TabIndex        =   234
         Text            =   "Text8"
         Top             =   1680
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.CommandButton Command11 
         Caption         =   "Command11"
         Height          =   615
         Left            =   2040
         TabIndex        =   233
         Top             =   0
         Visible         =   0   'False
         Width           =   1215
      End
      Begin VB.PictureBox Picture1 
         AutoSize        =   -1  'True
         Height          =   2895
         Left            =   0
         ScaleHeight     =   189
         ScaleMode       =   3  'Pixel
         ScaleWidth      =   221
         TabIndex        =   232
         Top             =   1920
         Visible         =   0   'False
         Width           =   3375
      End
      Begin VB.TextBox Text10 
         Height          =   375
         Left            =   3840
         TabIndex        =   231
         Text            =   "Text10"
         Top             =   3360
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.TextBox Text11 
         Height          =   285
         Left            =   2880
         TabIndex        =   230
         Text            =   "0"
         Top             =   840
         Visible         =   0   'False
         Width           =   495
      End
      Begin VB.TextBox Text12 
         Height          =   285
         Left            =   2880
         TabIndex        =   229
         Text            =   "0"
         Top             =   1440
         Visible         =   0   'False
         Width           =   495
      End
      Begin VB.TextBox Text13 
         Height          =   375
         Left            =   1560
         TabIndex        =   228
         Text            =   "100"
         Top             =   1200
         Visible         =   0   'False
         Width           =   495
      End
      Begin VB.TextBox Text15 
         Height          =   375
         Left            =   240
         TabIndex        =   227
         Text            =   "Text15"
         Top             =   1200
         Visible         =   0   'False
         Width           =   615
      End
      Begin VB.TextBox Text16 
         Height          =   375
         Left            =   3840
         TabIndex        =   226
         Text            =   "Text16"
         Top             =   2280
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.TextBox Text17 
         Height          =   375
         Left            =   3840
         TabIndex        =   225
         Text            =   "Text17"
         Top             =   2880
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.TextBox Text18 
         Height          =   375
         Left            =   240
         TabIndex        =   224
         Text            =   "1.5"
         Top             =   360
         Visible         =   0   'False
         Width           =   735
      End
      Begin VB.TextBox Text19 
         Height          =   375
         Left            =   1200
         TabIndex        =   223
         Text            =   "0.05"
         Top             =   360
         Visible         =   0   'False
         Width           =   735
      End
   End
   Begin VB.PictureBox Port_Warning 
      BackColor       =   &H000000FF&
      FillColor       =   &H00FFFFFF&
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   24
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H00FFFFFF&
      Height          =   255
      Left            =   6120
      ScaleHeight     =   195
      ScaleWidth      =   675
      TabIndex        =   221
      Top             =   8040
      Visible         =   0   'False
      Width           =   735
   End
   Begin VB.CommandButton Port_control 
      Caption         =   "Close Port"
      Height          =   495
      Left            =   7320
      TabIndex        =   220
      Top             =   7440
      Width           =   1095
   End
   Begin VB.Frame stage_frame 
      Caption         =   "Stage Movement"
      Height          =   255
      Left            =   4800
      TabIndex        =   73
      Top             =   7440
      Width           =   1485
      Begin VB.CommandButton StageMovementSwitch 
         Caption         =   "Stage"
         Height          =   375
         Left            =   3720
         TabIndex        =   74
         Top             =   120
         Visible         =   0   'False
         Width           =   1095
      End
      Begin VB.Frame stage_frame1 
         Caption         =   "Step1"
         Height          =   1695
         Left            =   120
         TabIndex        =   91
         Top             =   600
         Visible         =   0   'False
         Width           =   3135
         Begin VB.TextBox yinput1 
            Height          =   495
            Left            =   240
            TabIndex        =   103
            Top             =   840
            Width           =   1695
         End
         Begin VB.TextBox xinput1 
            Height          =   495
            Left            =   240
            TabIndex        =   102
            Top             =   240
            Width           =   1695
         End
         Begin VB.Label Label1 
            Caption         =   "X-Axis / "
            Height          =   375
            Left            =   2040
            TabIndex        =   93
            Top             =   480
            Width           =   855
         End
         Begin VB.Label Label2 
            Caption         =   "Y-Axis /"
            Height          =   255
            Left            =   2040
            TabIndex        =   92
            Top             =   1080
            Width           =   735
         End
      End
      Begin VB.Frame stage_frame2 
         Caption         =   "Step2"
         Height          =   1695
         Left            =   120
         TabIndex        =   84
         Top             =   2400
         Visible         =   0   'False
         Width           =   3135
         Begin VB.TextBox yinput2 
            Height          =   495
            Left            =   240
            TabIndex        =   106
            Top             =   840
            Width           =   1695
         End
         Begin VB.TextBox xinput2 
            Height          =   495
            Left            =   240
            TabIndex        =   85
            Top             =   240
            Width           =   1695
         End
         Begin VB.Label Label3 
            Caption         =   "X-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   87
            Top             =   480
            Width           =   735
         End
         Begin VB.Label Label4 
            Caption         =   "Y-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   86
            Top             =   1080
            Width           =   735
         End
      End
      Begin VB.Frame stage_frame3 
         Caption         =   "Step3"
         Height          =   1695
         Left            =   120
         TabIndex        =   81
         Top             =   4200
         Visible         =   0   'False
         Width           =   3135
         Begin VB.TextBox yinput3 
            Height          =   495
            Left            =   240
            TabIndex        =   110
            Top             =   840
            Width           =   1695
         End
         Begin VB.TextBox xinput3 
            Height          =   495
            Left            =   240
            TabIndex        =   109
            Top             =   240
            Width           =   1695
         End
         Begin VB.Label Label5 
            Caption         =   "X-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   83
            Top             =   480
            Width           =   855
         End
         Begin VB.Label Label6 
            Caption         =   "Y-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   82
            Top             =   1080
            Width           =   855
         End
      End
      Begin VB.Frame stage_frame4 
         Caption         =   "Step4"
         Height          =   1695
         Left            =   3240
         TabIndex        =   88
         Top             =   600
         Visible         =   0   'False
         Width           =   3135
         Begin VB.TextBox yinput4 
            Height          =   495
            Left            =   240
            TabIndex        =   105
            Top             =   840
            Width           =   1695
         End
         Begin VB.TextBox xinput4 
            Height          =   495
            Left            =   240
            TabIndex        =   104
            Top             =   240
            Width           =   1695
         End
         Begin VB.Label Label8 
            Caption         =   "Y-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   89
            Top             =   1080
            Width           =   855
         End
         Begin VB.Label Label7 
            Caption         =   "X-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   90
            Top             =   480
            Width           =   855
         End
      End
      Begin VB.Frame stage_frame5 
         Caption         =   "Step5"
         Height          =   1695
         Left            =   3120
         TabIndex        =   78
         Top             =   2400
         Visible         =   0   'False
         Width           =   3255
         Begin VB.TextBox yinput5 
            Height          =   495
            Left            =   360
            TabIndex        =   108
            Top             =   840
            Width           =   1695
         End
         Begin VB.TextBox xinput5 
            Height          =   495
            Left            =   360
            TabIndex        =   107
            Top             =   240
            Width           =   1695
         End
         Begin VB.Label Label10 
            Caption         =   "Y-Axis /"
            Height          =   375
            Left            =   2160
            TabIndex        =   79
            Top             =   1080
            Width           =   855
         End
         Begin VB.Label Label9 
            Caption         =   "X-Axis /"
            Height          =   375
            Left            =   2160
            TabIndex        =   80
            Top             =   480
            Width           =   855
         End
      End
      Begin VB.Frame stage_frame6 
         Caption         =   "Step6"
         Height          =   1695
         Left            =   3240
         TabIndex        =   75
         Top             =   4200
         Visible         =   0   'False
         Width           =   3135
         Begin VB.TextBox yinput6 
            Height          =   495
            Left            =   240
            TabIndex        =   112
            Top             =   840
            Width           =   1695
         End
         Begin VB.TextBox xinput6 
            Height          =   495
            Left            =   240
            TabIndex        =   111
            Top             =   240
            Width           =   1695
         End
         Begin VB.Label Label11 
            Caption         =   "X-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   77
            Top             =   600
            Width           =   855
         End
         Begin VB.Label Label12 
            Caption         =   "Y-Axis /"
            Height          =   375
            Left            =   2040
            TabIndex        =   76
            Top             =   1080
            Width           =   855
         End
      End
      Begin VB.Label Label_SM_direction 
         Caption         =   "Input Moving Direction for:"
         Height          =   375
         Left            =   1680
         TabIndex        =   94
         Top             =   240
         Visible         =   0   'False
         Width           =   1935
      End
   End
   Begin VB.CommandButton MoveMultiRastor 
      Caption         =   "Go Multi !"
      Height          =   495
      Left            =   7320
      TabIndex        =   213
      Top             =   6600
      Width           =   1095
   End
   Begin VB.Frame Warning_frame 
      Caption         =   "Warning"
      Height          =   255
      Left            =   3360
      TabIndex        =   117
      Top             =   7320
      Visible         =   0   'False
      Width           =   975
      Begin VB.CommandButton CloseWarning 
         Caption         =   "X"
         Height          =   255
         Left            =   2520
         TabIndex        =   118
         Top             =   0
         Width           =   255
      End
      Begin VB.Label WarningText 
         Alignment       =   2  'Center
         Caption         =   "Please Set Steps"
         Height          =   375
         Left            =   360
         TabIndex        =   119
         Top             =   480
         Width           =   2055
      End
   End
   Begin VB.CommandButton Command_Print_Pic 
      Caption         =   "Print Picture"
      Height          =   375
      Left            =   5520
      TabIndex        =   201
      Top             =   720
      Width           =   1215
   End
   Begin VB.Frame Advance_Option 
      Caption         =   "Advance Option"
      Height          =   255
      Left            =   3960
      TabIndex        =   197
      Top             =   7680
      Visible         =   0   'False
      Width           =   1335
      Begin VB.TextBox Text9 
         Height          =   375
         Left            =   1320
         TabIndex        =   219
         Text            =   "50"
         Top             =   1560
         Width           =   735
      End
      Begin VB.TextBox Text6 
         Height          =   375
         Left            =   1440
         TabIndex        =   215
         Text            =   "3333"
         Top             =   960
         Width           =   555
      End
      Begin VB.TextBox Text2 
         Height          =   375
         Left            =   720
         TabIndex        =   214
         Text            =   "200"
         Top             =   960
         Width           =   555
      End
      Begin VB.CheckBox Check1 
         Caption         =   "Check1"
         Height          =   435
         Left            =   1440
         TabIndex        =   203
         Top             =   360
         Width           =   255
      End
      Begin VB.CommandButton Command9 
         Caption         =   "X"
         Height          =   375
         Left            =   1920
         TabIndex        =   198
         Top             =   0
         Width           =   255
      End
      Begin VB.Label Label84 
         Caption         =   "Draw_mode2 Extra Boundry"
         Height          =   495
         Left            =   120
         TabIndex        =   218
         Top             =   1560
         Width           =   1095
      End
      Begin VB.Label Label83 
         Caption         =   "Test Mode"
         Height          =   255
         Left            =   360
         TabIndex        =   202
         Top             =   480
         Width           =   1095
      End
      Begin VB.Label Label82 
         Caption         =   "Power control reset mode"
         Height          =   315
         Left            =   180
         TabIndex        =   200
         Top             =   3120
         Width           =   1875
      End
      Begin VB.Label Label81 
         Caption         =   "Power control speed"
         Height          =   795
         Left            =   120
         TabIndex        =   199
         Top             =   840
         Width           =   615
      End
   End
   Begin VB.Frame Advance_Pass 
      Caption         =   "Advance"
      Height          =   255
      Left            =   180
      TabIndex        =   193
      Top             =   6060
      Visible         =   0   'False
      Width           =   855
      Begin VB.CommandButton Command8 
         Caption         =   "X"
         Height          =   315
         Left            =   2460
         TabIndex        =   196
         Top             =   0
         Width           =   255
      End
      Begin VB.TextBox Text5 
         Height          =   435
         Left            =   240
         TabIndex        =   195
         Top             =   720
         Width           =   2115
      End
      Begin VB.Label Label79 
         Caption         =   "Enter Password:"
         Height          =   255
         Left            =   120
         TabIndex        =   194
         Top             =   300
         Width           =   1335
      End
   End
   Begin VB.CommandButton Command7 
      Caption         =   "Command7"
      Height          =   495
      Left            =   0
      TabIndex        =   188
      Top             =   2580
      Visible         =   0   'False
      Width           =   1035
   End
   Begin VB.CommandButton Command6 
      Caption         =   "test shutter respond"
      Height          =   435
      Left            =   60
      TabIndex        =   187
      Top             =   7200
      Visible         =   0   'False
      Width           =   1275
   End
   Begin VB.CommandButton Command5 
      Caption         =   "Command5"
      Height          =   435
      Left            =   0
      TabIndex        =   184
      Top             =   3300
      Visible         =   0   'False
      Width           =   1035
   End
   Begin VB.Frame Print_Frame 
      Caption         =   "Print"
      Height          =   255
      Left            =   360
      TabIndex        =   176
      Top             =   3960
      Width           =   555
      Begin VB.ComboBox FontChoice 
         Height          =   315
         Left            =   2580
         TabIndex        =   185
         Text            =   "Choose Font"
         Top             =   420
         Width           =   1695
      End
      Begin VB.CommandButton StartPrint 
         Caption         =   "Print"
         Height          =   375
         Left            =   3240
         TabIndex        =   182
         Top             =   2160
         Visible         =   0   'False
         Width           =   735
      End
      Begin VB.TextBox PrintContant 
         Height          =   1095
         Left            =   420
         TabIndex        =   181
         Top             =   1440
         Width           =   2475
      End
      Begin VB.OptionButton Option_PrintType2 
         Caption         =   "Option2"
         Height          =   255
         Left            =   360
         TabIndex        =   179
         Top             =   960
         Width           =   255
      End
      Begin VB.OptionButton Option_PrintTpye1 
         Caption         =   "Option1"
         Height          =   255
         Left            =   360
         TabIndex        =   177
         Top             =   480
         Width           =   255
      End
      Begin VB.Label Label77 
         Caption         =   "Print Following Contant"
         Height          =   375
         Left            =   720
         TabIndex        =   180
         Top             =   960
         Width           =   1815
      End
      Begin VB.Label Label76 
         Caption         =   "Print While Typing"
         Height          =   375
         Left            =   720
         TabIndex        =   178
         Top             =   480
         Width           =   1935
      End
   End
   Begin VB.CommandButton Command_Print 
      Caption         =   "Printing"
      Height          =   375
      Left            =   2880
      TabIndex        =   152
      Top             =   720
      Width           =   1335
   End
   Begin VB.CommandButton Command_Shutter_Control 
      Caption         =   "Laser Control"
      Height          =   375
      Left            =   120
      TabIndex        =   151
      Top             =   720
      Width           =   1335
   End
   Begin VB.Frame MultiRastor 
      Caption         =   "Multi Rastor"
      Height          =   255
      Left            =   6360
      TabIndex        =   150
      Top             =   8880
      Width           =   1155
      Begin VB.CommandButton Command4 
         Caption         =   "Command4"
         Height          =   195
         Left            =   5580
         TabIndex        =   212
         Top             =   2220
         Width           =   135
      End
      Begin VB.TextBox MultiRastorWaiting 
         Height          =   375
         Left            =   4680
         TabIndex        =   207
         Top             =   2160
         Width           =   735
      End
      Begin VB.CommandButton Command_Close_Multi 
         Caption         =   "X"
         Height          =   315
         Left            =   5520
         TabIndex        =   205
         Top             =   0
         Width           =   255
      End
      Begin VB.TextBox ChangeSquareNum 
         Height          =   375
         Left            =   3600
         TabIndex        =   175
         Top             =   3600
         Width           =   855
      End
      Begin VB.CommandButton SetMultiRastorParameters 
         Caption         =   "Set Parameters"
         Height          =   495
         Left            =   4560
         TabIndex        =   173
         Top             =   2640
         Width           =   1095
      End
      Begin VB.TextBox MultiRastorEndPower 
         Height          =   405
         Left            =   3600
         TabIndex        =   172
         Top             =   2760
         Width           =   735
      End
      Begin VB.TextBox MultiRastorStartPower 
         Height          =   405
         Left            =   2520
         TabIndex        =   170
         Top             =   2760
         Width           =   735
      End
      Begin VB.CheckBox Check2 
         Caption         =   "Check2"
         Height          =   255
         Left            =   4620
         TabIndex        =   167
         Top             =   3720
         Width           =   255
      End
      Begin VB.TextBox SquareDimensionY 
         Height          =   405
         Left            =   2040
         TabIndex        =   165
         Top             =   1560
         Width           =   735
      End
      Begin VB.TextBox SquareDimensionX 
         Height          =   405
         Left            =   2040
         TabIndex        =   164
         Top             =   960
         Width           =   735
      End
      Begin VB.CommandButton MultiRastorDirection 
         Caption         =   "X"
         Height          =   375
         Left            =   2040
         TabIndex        =   161
         Top             =   2160
         Width           =   735
      End
      Begin VB.CommandButton MultiRastorOrder 
         Caption         =   "No. of Suqares/Row:"
         Height          =   255
         Left            =   2880
         TabIndex        =   160
         Top             =   360
         Width           =   1695
      End
      Begin VB.TextBox MultiRastorColSpacing 
         Height          =   405
         Left            =   4680
         TabIndex        =   159
         Top             =   1560
         Width           =   735
      End
      Begin VB.TextBox MultiRastorRowSpacing 
         Height          =   405
         Left            =   4680
         TabIndex        =   158
         Top             =   960
         Width           =   735
      End
      Begin VB.TextBox CharNumOfRastor 
         Height          =   405
         Left            =   4680
         TabIndex        =   155
         Top             =   360
         Width           =   735
      End
      Begin VB.TextBox MultiSquareNumber 
         Height          =   405
         Left            =   2040
         TabIndex        =   154
         Top             =   360
         Width           =   735
      End
      Begin VB.Label Label65 
         Caption         =   "Waiting Time:"
         Height          =   315
         Left            =   3000
         TabIndex        =   206
         Top             =   2160
         Width           =   1335
      End
      Begin VB.Label Label72 
         Caption         =   "View/Change Parameters For Square:"
         Height          =   375
         Left            =   360
         TabIndex        =   174
         Top             =   3600
         Width           =   3015
      End
      Begin VB.Line Line1 
         BorderColor     =   &H8000000A&
         X1              =   5760
         X2              =   0
         Y1              =   3360
         Y2              =   3360
      End
      Begin VB.Label Label75 
         Caption         =   "  To"
         Height          =   255
         Left            =   3240
         TabIndex        =   171
         Top             =   2760
         Width           =   495
      End
      Begin VB.Label Label71 
         Caption         =   "Power Linear Change From:"
         Height          =   255
         Left            =   360
         TabIndex        =   169
         Top             =   2760
         Width           =   2295
      End
      Begin VB.Label Label70 
         Caption         =   "With Index"
         Height          =   255
         Left            =   4500
         TabIndex        =   168
         Top             =   3480
         Width           =   1215
      End
      Begin VB.Label Label69 
         Caption         =   "Rastor Direction"
         Height          =   255
         Left            =   360
         TabIndex        =   166
         Top             =   2160
         Width           =   1455
      End
      Begin VB.Label Label68 
         Caption         =   "Square Dimension/Y"
         Height          =   255
         Left            =   360
         TabIndex        =   163
         Top             =   1560
         Width           =   1575
      End
      Begin VB.Label Label67 
         Caption         =   "Square Dimension/X"
         Height          =   255
         Left            =   360
         TabIndex        =   162
         Top             =   960
         Width           =   1575
      End
      Begin VB.Label Label74 
         Caption         =   "Spacing of Clos:"
         Height          =   255
         Left            =   3000
         TabIndex        =   157
         Top             =   1560
         Width           =   1335
      End
      Begin VB.Label Label73 
         Caption         =   "Spacing of Rows:"
         Height          =   255
         Left            =   3000
         TabIndex        =   156
         Top             =   960
         Width           =   1455
      End
      Begin VB.Label Label58 
         Caption         =   "Total No. of Squares:"
         Height          =   255
         Left            =   360
         TabIndex        =   153
         Top             =   360
         Width           =   1575
      End
   End
   Begin VB.Frame shutterControl 
      Caption         =   "Shutter Control"
      Height          =   255
      Left            =   0
      TabIndex        =   142
      Top             =   6420
      Width           =   1215
      Begin VB.CommandButton shutterControlOperate 
         Caption         =   "Operate"
         Height          =   375
         Left            =   720
         TabIndex        =   149
         Top             =   1800
         Width           =   1095
      End
      Begin VB.TextBox ShutterOffTimeValue 
         Height          =   285
         Left            =   1560
         TabIndex        =   148
         Text            =   "1"
         Top             =   1320
         Width           =   735
      End
      Begin VB.TextBox ShutterOnTimeValue 
         Height          =   285
         Left            =   1560
         TabIndex        =   147
         Text            =   "1"
         Top             =   840
         Width           =   735
      End
      Begin VB.TextBox ShutterLoopValue 
         Height          =   285
         Left            =   1560
         TabIndex        =   146
         Text            =   "1"
         Top             =   360
         Width           =   735
      End
      Begin VB.Label ShutterOffTime 
         Caption         =   "OffTime"
         Height          =   375
         Left            =   240
         TabIndex        =   145
         Top             =   1320
         Width           =   975
      End
      Begin VB.Label ShutterOnTime 
         Caption         =   "On time"
         Height          =   375
         Left            =   240
         TabIndex        =   144
         Top             =   840
         Width           =   975
      End
      Begin VB.Label ShutterLoop 
         Caption         =   "Loop Num."
         Height          =   375
         Left            =   240
         TabIndex        =   143
         Top             =   360
         Width           =   855
      End
   End
   Begin VB.CommandButton Command3 
      Caption         =   "test Stage"
      Height          =   495
      Left            =   0
      TabIndex        =   141
      Top             =   1800
      Width           =   1035
   End
   Begin VB.Frame drawPic_frame 
      Caption         =   "Draw Picture"
      Height          =   3615
      Left            =   2040
      TabIndex        =   127
      Top             =   2520
      Visible         =   0   'False
      Width           =   3735
      Begin VB.CommandButton Drawpic_Load 
         Caption         =   "Load"
         Height          =   255
         Left            =   2880
         TabIndex        =   248
         Top             =   3240
         Width           =   735
      End
      Begin VB.CommandButton Drawpic_Save 
         Caption         =   "Save"
         Height          =   255
         Left            =   2040
         TabIndex        =   247
         Top             =   3240
         Width           =   735
      End
      Begin VB.PictureBox DrawPicProgress 
         BackColor       =   &H00000000&
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   9.75
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H0000FF00&
         Height          =   375
         Left            =   2040
         ScaleHeight     =   315
         ScaleWidth      =   1515
         TabIndex        =   246
         Top             =   1560
         Width           =   1575
      End
      Begin VB.CommandButton DrawPicPause 
         Caption         =   "Pause"
         Height          =   375
         Left            =   120
         TabIndex        =   245
         Top             =   2040
         Width           =   1695
      End
      Begin VB.TextBox DrawPicStepX 
         Height          =   285
         Left            =   1200
         TabIndex        =   243
         Text            =   "1"
         Top             =   3240
         Width           =   615
      End
      Begin VB.TextBox DrawPicMax 
         Height          =   285
         Left            =   2760
         TabIndex        =   240
         Text            =   "200"
         Top             =   2880
         Width           =   855
      End
      Begin VB.TextBox DrawPicMin 
         Height          =   285
         Left            =   1560
         TabIndex        =   239
         Text            =   "-1"
         Top             =   2880
         Width           =   855
      End
      Begin VB.TextBox Text20 
         Height          =   375
         Left            =   2040
         TabIndex        =   238
         Top             =   360
         Width           =   1575
      End
      Begin VB.OptionButton Pic_mode2 
         Caption         =   "Drawing Mode2"
         Height          =   375
         Left            =   2160
         TabIndex        =   217
         Top             =   2520
         Width           =   1575
      End
      Begin VB.OptionButton Pic_mode1 
         Caption         =   "Drawing Mode1"
         Height          =   375
         Left            =   360
         TabIndex        =   216
         Top             =   2520
         Width           =   1455
      End
      Begin VB.TextBox correction 
         Height          =   375
         Left            =   2280
         TabIndex        =   192
         Top             =   3840
         Width           =   975
      End
      Begin VB.TextBox Text14 
         Height          =   375
         Left            =   2040
         TabIndex        =   186
         Text            =   "1"
         Top             =   2040
         Width           =   735
      End
      Begin VB.CommandButton StartDrawColor 
         Caption         =   "Start Draw Color"
         Height          =   375
         Left            =   240
         TabIndex        =   140
         Top             =   3600
         Visible         =   0   'False
         Width           =   1815
      End
      Begin VB.TextBox Text1 
         Height          =   375
         Left            =   2880
         TabIndex        =   132
         Top             =   2040
         Width           =   735
      End
      Begin VB.CommandButton StartDraw 
         Caption         =   "Start Drawing"
         Height          =   375
         Left            =   120
         TabIndex        =   131
         Top             =   1560
         Width           =   1695
      End
      Begin VB.PictureBox drawPicStatus 
         BackColor       =   &H00000000&
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   9.75
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H0000FF00&
         Height          =   375
         Left            =   2040
         ScaleHeight     =   315
         ScaleWidth      =   1515
         TabIndex        =   129
         Top             =   1080
         Width           =   1575
      End
      Begin VB.CommandButton input_pic 
         Caption         =   "Input Picture"
         Height          =   375
         Left            =   120
         TabIndex        =   128
         Top             =   1080
         Width           =   1695
      End
      Begin VB.Label Label20 
         Caption         =   "Image Range:"
         Height          =   255
         Left            =   240
         TabIndex        =   244
         Top             =   2880
         Width           =   1215
      End
      Begin VB.Label Label19 
         Caption         =   "X Step Size:"
         Height          =   255
         Left            =   240
         TabIndex        =   242
         Top             =   3240
         Width           =   975
      End
      Begin VB.Label Label18 
         Caption         =   "File Name:            (without .bmp)"
         Height          =   375
         Left            =   240
         TabIndex        =   237
         Top             =   360
         Width           =   1695
      End
      Begin VB.Label lablePicStauts 
         Caption         =   "Status"
         Height          =   375
         Left            =   2640
         TabIndex        =   130
         Top             =   840
         Width           =   615
      End
   End
   Begin VB.CommandButton Laser_Close 
      BackColor       =   &H008080FF&
      Caption         =   "Close"
      Height          =   375
      Left            =   6120
      TabIndex        =   126
      Top             =   8400
      Width           =   615
   End
   Begin VB.CommandButton Laser_Open 
      BackColor       =   &H0080FF80&
      Caption         =   "Open"
      Height          =   375
      Left            =   1440
      TabIndex        =   125
      Top             =   8400
      Width           =   4695
   End
   Begin VB.Frame test_frame 
      Caption         =   "test"
      Height          =   315
      Left            =   60
      TabIndex        =   95
      Top             =   4260
      Width           =   615
      Begin VB.CommandButton testFinal 
         Caption         =   "Test Final"
         Height          =   375
         Left            =   3360
         TabIndex        =   116
         Top             =   840
         Width           =   855
      End
      Begin VB.CommandButton TestStepShake 
         Caption         =   "Shake"
         Height          =   495
         Left            =   3480
         TabIndex        =   115
         Top             =   3960
         Width           =   975
      End
      Begin VB.CommandButton TestStepAnother 
         Caption         =   "Another direction"
         Height          =   495
         Left            =   3480
         TabIndex        =   114
         Top             =   3120
         Width           =   975
      End
      Begin VB.CommandButton TestStepOne 
         Caption         =   "One direction"
         Height          =   495
         Left            =   3480
         TabIndex        =   113
         Top             =   2280
         Width           =   975
      End
      Begin VB.TextBox Freq 
         Height          =   375
         Left            =   2400
         TabIndex        =   101
         Top             =   2880
         Width           =   975
      End
      Begin VB.CommandButton StopStep 
         Caption         =   "Stop Step"
         Height          =   375
         Left            =   840
         TabIndex        =   100
         Top             =   3600
         Width           =   975
      End
      Begin VB.CommandButton TestStep 
         Caption         =   "TestStep"
         Height          =   375
         Left            =   840
         TabIndex        =   99
         Top             =   2760
         Width           =   975
      End
      Begin VB.TextBox watchi 
         Height          =   375
         Left            =   2280
         TabIndex        =   98
         Top             =   1440
         Width           =   615
      End
      Begin VB.TextBox debugText 
         Height          =   375
         Left            =   2280
         TabIndex        =   97
         Top             =   600
         Width           =   615
      End
      Begin VB.CommandButton testTimeComd 
         Caption         =   "TestTime"
         Height          =   495
         Left            =   840
         TabIndex        =   96
         Top             =   600
         Width           =   855
      End
   End
   Begin VB.Frame laser_power_frame 
      Caption         =   "Power Control"
      Height          =   255
      Left            =   1680
      TabIndex        =   120
      Top             =   7860
      Width           =   1215
      Begin VB.CommandButton Command2 
         Caption         =   "Set Zero"
         Height          =   375
         Left            =   1500
         TabIndex        =   139
         Top             =   2400
         Width           =   1215
      End
      Begin VB.TextBox Text4 
         Height          =   315
         Left            =   300
         TabIndex        =   138
         Text            =   "0"
         Top             =   1800
         Width           =   855
      End
      Begin VB.TextBox Text3 
         Height          =   315
         Left            =   1500
         TabIndex        =   137
         Text            =   "0"
         Top             =   840
         Width           =   855
      End
      Begin VB.CommandButton Command1 
         Caption         =   "Go to step"
         Height          =   315
         Left            =   1500
         TabIndex        =   135
         Top             =   1800
         Width           =   915
      End
      Begin VB.CommandButton flag_laser 
         Caption         =   "Flag Laser"
         Height          =   375
         Left            =   240
         TabIndex        =   123
         Top             =   2400
         Width           =   975
      End
      Begin VB.TextBox CurrentAngle 
         Height          =   315
         Left            =   1500
         TabIndex        =   122
         Text            =   "0"
         Top             =   1260
         Width           =   855
      End
      Begin VB.TextBox MotorStep 
         Height          =   315
         Left            =   1500
         TabIndex        =   121
         Text            =   "1"
         Top             =   360
         Width           =   855
      End
      Begin VB.Label Label50 
         Caption         =   "Total step"
         Height          =   255
         Left            =   300
         TabIndex        =   136
         Top             =   840
         Width           =   975
      End
      Begin VB.Label Label49 
         Caption         =   "Total angle"
         Height          =   255
         Left            =   300
         TabIndex        =   134
         Top             =   1320
         Width           =   915
      End
      Begin VB.Label Label48 
         Caption         =   "Step Size"
         Height          =   255
         Left            =   300
         TabIndex        =   133
         Top             =   360
         Width           =   795
      End
   End
   Begin VB.Frame arrow_frame 
      Caption         =   "Arrow Control"
      Height          =   255
      Left            =   1560
      TabIndex        =   50
      Top             =   7080
      Visible         =   0   'False
      Width           =   1215
      Begin VB.CommandButton RunToCor 
         Caption         =   "Run To (X,Y)"
         Height          =   375
         Left            =   2520
         TabIndex        =   183
         Top             =   2640
         Width           =   1215
      End
      Begin VB.CommandButton SetCor 
         Caption         =   "Set (X,Y)"
         Height          =   375
         Left            =   600
         TabIndex        =   72
         Top             =   2640
         Width           =   1215
      End
      Begin VB.TextBox CorYV 
         Height          =   375
         Left            =   2640
         TabIndex        =   69
         Text            =   "0"
         Top             =   2160
         Width           =   975
      End
      Begin VB.TextBox CorXV 
         Height          =   375
         Left            =   720
         TabIndex        =   68
         Text            =   "0"
         Top             =   2160
         Width           =   975
      End
      Begin VB.CommandButton origion 
         Caption         =   "Reset As ( 0 , 0 )"
         Height          =   495
         Left            =   2160
         TabIndex        =   61
         Top             =   1440
         Width           =   1815
      End
      Begin VB.TextBox AccuracyStep 
         Height          =   375
         Left            =   3000
         TabIndex        =   58
         Top             =   840
         Width           =   615
      End
      Begin VB.PictureBox arrowYpic 
         BackColor       =   &H00000000&
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H0000FF00&
         Height          =   375
         Left            =   480
         ScaleHeight     =   315
         ScaleWidth      =   915
         TabIndex        =   56
         Top             =   1560
         Width           =   975
      End
      Begin VB.PictureBox arrowXpic 
         BackColor       =   &H00000000&
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H0000FF00&
         Height          =   375
         Left            =   480
         ScaleHeight     =   315
         ScaleWidth      =   915
         TabIndex        =   55
         Top             =   840
         Width           =   975
      End
      Begin VB.CommandButton ArrowControlSwitch 
         Caption         =   "Command4"
         Height          =   375
         Left            =   1560
         TabIndex        =   52
         Top             =   240
         Width           =   1095
      End
      Begin VB.Label CorY 
         Caption         =   "Y"
         Height          =   255
         Left            =   2280
         TabIndex        =   71
         Top             =   2160
         Width           =   255
      End
      Begin VB.Label CorX 
         Caption         =   "X"
         Height          =   255
         Left            =   480
         TabIndex        =   70
         Top             =   2160
         Width           =   135
      End
      Begin VB.Label Label64 
         Caption         =   "m"
         Height          =   255
         Left            =   1680
         TabIndex        =   65
         Top             =   1560
         Width           =   135
      End
      Begin VB.Label Label63 
         Caption         =   "m"
         BeginProperty Font 
            Name            =   "Symbol"
            Size            =   8.25
            Charset         =   2
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   375
         Left            =   1560
         TabIndex        =   64
         Top             =   1560
         Width           =   135
      End
      Begin VB.Label Label62 
         Caption         =   "m"
         Height          =   255
         Left            =   1680
         TabIndex        =   63
         Top             =   840
         Width           =   135
      End
      Begin VB.Label Label61 
         Caption         =   "m"
         BeginProperty Font 
            Name            =   "Symbol"
            Size            =   8.25
            Charset         =   2
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   1560
         TabIndex        =   62
         Top             =   840
         Width           =   135
      End
      Begin VB.Label Label60 
         Caption         =   "m"
         Height          =   255
         Left            =   3840
         TabIndex        =   60
         Top             =   840
         Width           =   135
      End
      Begin VB.Label Label59 
         Caption         =   "m"
         BeginProperty Font 
            Name            =   "Symbol"
            Size            =   8.25
            Charset         =   2
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   3720
         TabIndex        =   59
         Top             =   840
         Width           =   135
      End
      Begin VB.Label accuracy 
         Caption         =   "Accuracy"
         Height          =   375
         Left            =   2160
         TabIndex        =   57
         Top             =   840
         Width           =   735
      End
      Begin VB.Label disY 
         Caption         =   "Y"
         Height          =   375
         Left            =   240
         TabIndex        =   54
         Top             =   1560
         Width           =   375
      End
      Begin VB.Label disX 
         Caption         =   "X"
         Height          =   375
         Left            =   240
         TabIndex        =   53
         Top             =   840
         Width           =   255
      End
      Begin VB.Label displacement 
         Caption         =   "Displacement of:"
         Height          =   375
         Left            =   240
         TabIndex        =   51
         Top             =   360
         Width           =   1335
      End
   End
   Begin VB.CommandButton StopMusic 
      Caption         =   "Stop Music"
      Height          =   375
      Left            =   7320
      TabIndex        =   67
      Top             =   5880
      Width           =   1095
   End
   Begin VB.Frame rastor_frame 
      Caption         =   "Rastor"
      Height          =   255
      Left            =   240
      TabIndex        =   30
      Top             =   5520
      Visible         =   0   'False
      Width           =   675
      Begin VB.CommandButton MultiRastorSet 
         Caption         =   "Set"
         Height          =   375
         Left            =   3660
         TabIndex        =   211
         Top             =   2040
         Width           =   555
      End
      Begin VB.CommandButton MultiRastorView 
         Caption         =   "View"
         Height          =   375
         Left            =   3660
         TabIndex        =   210
         Top             =   1380
         Width           =   555
      End
      Begin VB.TextBox MultiRastorCurrentIndex 
         Height          =   435
         Left            =   3600
         TabIndex        =   209
         Top             =   720
         Width           =   675
      End
      Begin VB.CommandButton Command_Multi_Rastor 
         Caption         =   "Multi"
         Height          =   375
         Left            =   3000
         TabIndex        =   204
         Top             =   2700
         Width           =   495
      End
      Begin VB.TextBox AddtionDelayTime 
         Height          =   375
         Left            =   1740
         TabIndex        =   189
         Top             =   2700
         Width           =   915
      End
      Begin VB.TextBox step2 
         Height          =   495
         Left            =   2280
         TabIndex        =   42
         Top             =   1680
         Visible         =   0   'False
         Width           =   975
      End
      Begin VB.TextBox step1 
         Height          =   495
         Left            =   2280
         TabIndex        =   41
         Top             =   720
         Visible         =   0   'False
         Width           =   975
      End
      Begin VB.CheckBox rustY 
         Caption         =   "Check2"
         Height          =   255
         Left            =   1800
         TabIndex        =   40
         Top             =   1800
         Width           =   255
      End
      Begin VB.CheckBox rustX 
         Caption         =   "Check1"
         Height          =   495
         Left            =   1800
         TabIndex        =   39
         Top             =   720
         Width           =   255
      End
      Begin VB.TextBox yinputR 
         Height          =   495
         Left            =   240
         TabIndex        =   38
         Top             =   1680
         Width           =   1455
      End
      Begin VB.TextBox xinputR 
         Height          =   495
         Left            =   240
         TabIndex        =   37
         Top             =   720
         Width           =   1455
      End
      Begin VB.Label Label80 
         Caption         =   "Current Index"
         Height          =   435
         Left            =   3660
         TabIndex        =   208
         Top             =   300
         Width           =   615
      End
      Begin VB.Label Label78 
         Caption         =   "ms"
         Height          =   315
         Left            =   2700
         TabIndex        =   191
         Top             =   2760
         Width           =   435
      End
      Begin VB.Label AddDelay 
         Caption         =   "Additional delay time"
         Height          =   315
         Left            =   180
         TabIndex        =   190
         Top             =   2760
         Width           =   1515
      End
      Begin VB.Label Label66 
         Caption         =   "Draw a rectangle"
         Height          =   375
         Left            =   2160
         TabIndex        =   66
         Top             =   1320
         Visible         =   0   'False
         Width           =   1215
      End
      Begin VB.Label Label57 
         Caption         =   "Moving direction of Laser spot"
         Height          =   375
         Left            =   360
         TabIndex        =   47
         Top             =   240
         Width           =   1335
      End
      Begin VB.Label Label56 
         Caption         =   "Rastor"
         Height          =   375
         Left            =   2520
         TabIndex        =   46
         Top             =   360
         Visible         =   0   'False
         Width           =   615
      End
      Begin VB.Label Label55 
         Caption         =   "Draw a Line"
         Height          =   495
         Left            =   2280
         TabIndex        =   45
         Top             =   1320
         Width           =   855
      End
      Begin VB.Label Label54 
         Caption         =   "Step"
         Height          =   255
         Left            =   2280
         TabIndex        =   44
         Top             =   2280
         Visible         =   0   'False
         Width           =   615
      End
      Begin VB.Label Label53 
         Caption         =   "Step"
         Height          =   255
         Left            =   2280
         TabIndex        =   43
         Top             =   1320
         Visible         =   0   'False
         Width           =   495
      End
      Begin VB.Label Label52 
         Caption         =   "m"
         Height          =   255
         Left            =   960
         TabIndex        =   36
         Top             =   2280
         Width           =   135
      End
      Begin VB.Label Label51 
         Caption         =   "m"
         BeginProperty Font 
            Name            =   "Symbol"
            Size            =   8.25
            Charset         =   2
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   840
         TabIndex        =   35
         Top             =   2280
         Width           =   135
      End
      Begin VB.Label Label45 
         Caption         =   "Y-Axis /"
         Height          =   255
         Left            =   240
         TabIndex        =   34
         Top             =   2280
         Width           =   735
      End
      Begin VB.Label Label44 
         Caption         =   "m"
         Height          =   255
         Left            =   960
         TabIndex        =   33
         Top             =   1320
         Width           =   135
      End
      Begin VB.Label Label43 
         Caption         =   "m"
         BeginProperty Font 
            Name            =   "Symbol"
            Size            =   8.25
            Charset         =   2
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   255
         Left            =   840
         TabIndex        =   32
         Top             =   1320
         Width           =   135
      End
      Begin VB.Label Label42 
         Caption         =   "X-Axis / "
         Height          =   495
         Left            =   240
         TabIndex        =   31
         Top             =   1320
         Width           =   855
      End
   End
   Begin VB.PictureBox arrowpic 
      BackColor       =   &H00000000&
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H0000FF00&
      Height          =   375
      Left            =   6960
      ScaleHeight     =   315
      ScaleWidth      =   795
      TabIndex        =   49
      Top             =   120
      Width           =   855
   End
   Begin VB.CommandButton arrow 
      Caption         =   "Arrow Control"
      Height          =   375
      Left            =   5520
      TabIndex        =   48
      Top             =   120
      Width           =   1215
   End
   Begin VB.PictureBox rastorpic 
      BackColor       =   &H00000000&
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H0000FF00&
      Height          =   375
      Left            =   4440
      ScaleHeight     =   315
      ScaleWidth      =   795
      TabIndex        =   29
      Top             =   120
      Width           =   855
   End
   Begin VB.PictureBox stagepic 
      BackColor       =   &H00000000&
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H0000FF00&
      Height          =   375
      Left            =   1680
      ScaleHeight     =   315
      ScaleWidth      =   795
      TabIndex        =   28
      Top             =   120
      Width           =   855
   End
   Begin VB.CommandButton rastor 
      Caption         =   "raster"
      Height          =   375
      Left            =   2880
      TabIndex        =   27
      Top             =   120
      Width           =   1335
   End
   Begin VB.CommandButton stage 
      Caption         =   "stage movement"
      Height          =   375
      Left            =   120
      TabIndex        =   26
      Top             =   120
      Width           =   1335
   End
   Begin VB.CommandButton Abort 
      Caption         =   "Abort"
      Height          =   375
      Left            =   7320
      TabIndex        =   25
      Top             =   5160
      Width           =   1095
   End
   Begin VB.TextBox Tinput1 
      Height          =   285
      Left            =   7320
      TabIndex        =   24
      Text            =   "0"
      Top             =   3240
      Visible         =   0   'False
      Width           =   855
   End
   Begin VB.TextBox sec 
      Height          =   375
      Left            =   3360
      TabIndex        =   21
      Text            =   "0"
      Top             =   9000
      Width           =   735
   End
   Begin VB.TextBox min 
      Height          =   375
      Left            =   1800
      TabIndex        =   19
      Text            =   "0"
      Top             =   9000
      Width           =   735
   End
   Begin VB.TextBox hour 
      Height          =   375
      Left            =   360
      TabIndex        =   17
      Text            =   "0"
      Top             =   9000
      Width           =   735
   End
   Begin VB.Timer Timer1 
      Enabled         =   0   'False
      Interval        =   1000
      Left            =   7920
      Top             =   9000
   End
   Begin VB.TextBox XLoop 
      Height          =   375
      Left            =   2880
      TabIndex        =   15
      Top             =   1320
      Visible         =   0   'False
      Width           =   975
   End
   Begin MSCommLib.MSComm MSComm1 
      Left            =   8040
      Top             =   1320
      _ExtentX        =   1005
      _ExtentY        =   1005
      _Version        =   393216
      DTREnable       =   -1  'True
   End
   Begin VB.CommandButton Exit 
      Caption         =   "Exit"
      Height          =   495
      Left            =   7320
      TabIndex        =   11
      Top             =   8280
      Width           =   1095
   End
   Begin VB.CommandButton reset 
      Caption         =   "&Reset"
      Height          =   375
      Left            =   7320
      TabIndex        =   8
      Top             =   4440
      Width           =   1095
   End
   Begin VB.PictureBox ypic 
      BackColor       =   &H00000000&
      ForeColor       =   &H0000FF00&
      Height          =   375
      Left            =   7320
      ScaleHeight     =   315
      ScaleWidth      =   795
      TabIndex        =   7
      Top             =   2280
      Width           =   855
   End
   Begin VB.CommandButton Go 
      Caption         =   "Go"
      Height          =   375
      Left            =   1800
      TabIndex        =   4
      Top             =   1320
      Visible         =   0   'False
      Width           =   735
   End
   Begin VB.CommandButton MoveStart 
      Caption         =   "&Move"
      Height          =   495
      Left            =   7320
      TabIndex        =   3
      Top             =   6600
      Visible         =   0   'False
      Width           =   1095
   End
   Begin VB.ComboBox Steps 
      Height          =   315
      Left            =   120
      TabIndex        =   1
      Text            =   "# of Steps"
      Top             =   1320
      Visible         =   0   'False
      Width           =   1575
   End
   Begin VB.TextBox velocity 
      Height          =   375
      Left            =   5400
      TabIndex        =   0
      Top             =   1320
      Visible         =   0   'False
      Width           =   975
   End
   Begin VB.PictureBox picLogo 
      Height          =   375
      Left            =   120
      ScaleHeight     =   315
      ScaleWidth      =   855
      TabIndex        =   12
      Top             =   4920
      Width           =   915
      Begin VB.Label Label47 
         Caption         =   "COLLOID LAB"
         BeginProperty Font 
            Name            =   "Arial"
            Size            =   39.75
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H000080FF&
         Height          =   1335
         Left            =   360
         TabIndex        =   14
         Top             =   2640
         Width           =   6495
      End
      Begin VB.Label Label46 
         Caption         =   "NUS"
         BeginProperty Font 
            Name            =   "Arial"
            Size            =   36
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H00C00000&
         Height          =   855
         Left            =   360
         TabIndex        =   13
         Top             =   1560
         Width           =   1575
      End
   End
   Begin VB.Label label_laserShutter 
      Alignment       =   2  'Center
      Caption         =   "Laser Shutter"
      Height          =   255
      Left            =   180
      TabIndex        =   124
      Top             =   8460
      Width           =   1035
   End
   Begin VB.Label Time 
      Caption         =   "Time Remaining"
      Height          =   375
      Left            =   4920
      TabIndex        =   23
      Top             =   9000
      Width           =   1455
   End
   Begin VB.Label Label_sec 
      Caption         =   "sec"
      Height          =   255
      Left            =   4080
      TabIndex        =   22
      Top             =   9000
      Width           =   615
   End
   Begin VB.Label Label_min 
      Caption         =   "min"
      Height          =   255
      Left            =   2520
      TabIndex        =   20
      Top             =   9000
      Width           =   375
   End
   Begin VB.Label Label_hour 
      Caption         =   "h"
      Height          =   255
      Left            =   1080
      TabIndex        =   18
      Top             =   9000
      Width           =   255
   End
   Begin VB.Label LoopNum 
      Caption         =   "Loop.Num"
      Height          =   375
      Left            =   4080
      TabIndex        =   16
      Top             =   1320
      Visible         =   0   'False
      Width           =   735
   End
   Begin VB.Label Label17 
      Caption         =   "m/sec"
      Height          =   255
      Left            =   7200
      TabIndex        =   10
      Top             =   1320
      Visible         =   0   'False
      Width           =   735
   End
   Begin VB.Label Label16 
      Caption         =   "m"
      BeginProperty Font 
         Name            =   "Symbol"
         Size            =   8.25
         Charset         =   2
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   255
      Left            =   7080
      TabIndex        =   9
      Top             =   1320
      Visible         =   0   'False
      Width           =   135
   End
   Begin VB.Label Label15 
      Caption         =   "Status"
      Height          =   375
      Left            =   7320
      TabIndex        =   6
      Top             =   1800
      Width           =   1335
   End
   Begin VB.Label Label14 
      Caption         =   "Current Loop"
      Height          =   255
      Left            =   7320
      TabIndex        =   5
      Top             =   2760
      Visible         =   0   'False
      Width           =   1335
   End
   Begin VB.Label Label13 
      Caption         =   "Velocity"
      Height          =   375
      Left            =   6480
      TabIndex        =   2
      Top             =   1320
      Visible         =   0   'False
      Width           =   615
   End
End
Attribute VB_Name = "StageControl"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Dim X1, Y1, sent, enter, blank, run, vel As String
Dim V1, V2, V3, V4, V5, V6, VR As String
Dim X2, Y2, X3, Y3, X4, Y4, X5, Y5, X6, Y6 As String
Dim X1n, Y1n, X2n, Y2n, X3n, Y3n, X4n, Y4n, X5n, Y5n, X6n, Y6n As String
Dim XR, YR, XRn, YRn As String
Dim LN, stepsize, zero, stepsizen As String
Dim checkX, checkY As Integer
Dim i As Integer
Dim launchme, launch1, launch2, launch3, launch4, launch5, launch6 As String
'Dim xunit1, xunit2, xunit3, xunit4, xunit5, xunit6, velunit As String
'Dim yunit1, yunit2, yunit3, yunit4, yunit5, yunit6, sendlimit As String
Dim xuuniy, yunit, velunit As String
Dim xmove, ymove As Integer
Dim t, Tx, Ty, T1, T2, T3, T4, T5, T6, TR, Tsingle, Tsingle1, Txy1, Txy2 As Double
Dim flagStop As Integer
Dim flagMode As Integer
Dim flagSound As Integer
Dim flagStage As Integer
Dim flagDisStage As Integer
Dim temp, temp2 As String
Dim positionX, positionY As Integer
Dim flagDelay As Integer
Dim acStep As Integer
Dim tempVS, tempVR, tempVA As Integer
Dim aM, aMn As String 'arrowMove, arrowMovenegative
Dim arrowStepTime As Double
Dim flagFirst As Integer
Dim flagArrowKey As Integer
Dim flagToyBox As Integer
'Dim circleXP, circleYP As Integer
'Dim circleSX, circleSY, circleSXn, circleSYn As Integer
'Dim ScircleSX, ScircleSY, ScircleSXn, ScircleSYn As String 'to start circle, move this amount
'Dim flagCircleFirst As Integer
'Dim tempRadius, CurrentRadius As Double
'Dim flagStartingPoint As Integer
'Dim DrawRadius As Integer
'Dim circleAimX, circleAimY, circleMoveX, circleMoveY As Integer
'Dim circleSingleT, calT As Double
'Dim TcircleAimX, TcircleAimY, TcircleMoveX, TcircleMoveY, TcircleXP, TcircleYP As Integer
'Dim circleMoveXS, circleMoveYS As String
Dim test1, test2, test3 As Double
Dim StepFreq As Integer
Dim flagStopStep As Integer
Dim flagWarning As Integer
Dim laserStep As Integer
Dim laserPosition As Double
Dim pixelPannel() As Integer
Dim newPixelPannel() As Integer
Dim picWidth As Long
Dim picHeight As Long
Dim shutterIsOpen As Boolean
Dim goToStepNum As Integer
Dim totalStep As Integer
Dim changeStep As Integer
Dim picRegionMax As Integer
Dim picRegionMin As Integer
Dim picRegionWhite As Integer
Dim drawLength As Integer
Dim picDrawCorrect As Double
Dim laserPrintContent As String
Dim shutterControlLoop As Integer
Dim ShutterControlOnTime, ShutterControlOffTime As Double
'Dim laserPrintContentArray() As Chr
Dim flagPrintMode As Integer
Dim flagPrintEnd As Boolean
Dim WorldX, WorldY As Integer '(in the stage of view)
Dim FontPixel() As Integer
Dim FontLocation() As Font
Dim fontDrawCorrect As Integer
Dim countFontCorrect As Integer
Dim fontWidth, fontHeight As Integer
Dim printType1, printType2 As Boolean
Dim AddDelayTime As Integer
Dim testCorrection As Double
Dim drawregioni As Integer
Dim flagMultiDirection As Integer   '1 for X, 2 for Y
Dim flagMultiOrder As Integer       '1 for row, 2 for col
Dim totalMultiNum As Integer
Dim flagMultiRastor As Boolean
Dim laserMotorFreq As Integer
Dim allowPowerChange As Boolean
Dim powerStepDelay As Integer
Dim print_content() As String
Dim drawing_mode As Integer
Dim DrawPicExtraBoundry As Integer
Dim flagDrawPicPause1 As Boolean
Dim DrawPicStartValue As Integer
Dim DrawPicTime1 As Double
Dim flagDrawpicAbort1 As Boolean

Private Declare Function GetDC Lib "user32" (ByVal hwnd As Long) As Long
Private Declare Function ReleaseDC Lib "user32" (ByVal hwnd As Long, ByVal hdc As Long) As Long

Private Declare Function BitBlt Lib "gdi32" _
(ByVal hDestDC As Long, ByVal X As Long, _
ByVal Y As Long, ByVal nWidth As Long, _
ByVal nHeight As Long, ByVal hSrcDC As Long, _
ByVal xSrc As Long, ByVal ySrc As Long, _
ByVal dwRop As Long) As Long


Private Declare Sub out Lib "inpout32.dll" Alias "Out32" (ByVal PortAddress As Integer, ByVal Value As Integer)
Private Declare Function QueryPerformanceCounter Lib "kernel32" (IpPerformanceCount As Currency) As Long
Private Declare Function QueryPerformanceFrequency Lib "kernel32" (IpFrequency As Currency) As Long
Private Declare Sub Sleep Lib "kernel32" (ByVal dwMilliseconds As Long)
Private Declare Function timeGetTime Lib "winmm.dll" () As Long
Private Declare Function sndPlaySound Lib "winmm.dll" Alias _
    "sndPlaySoundA" (ByVal lpszSoundName As String, ByVal uFlags As _
      Long) As Long
   Const SND_SYNC = &H0
   Const SND_ASYNC = &H1
   Const SND_NODEFAULT = &H2
   Const SND_LOOP = &H8
   Const SND_NOSTOP = &H10




Private Declare Function DeleteDC Lib "gdi32" (ByVal hdc As Long) As Long
Private Declare Function DeleteObject Lib "gdi32" (ByVal hObject As Long) As Long
Private Declare Function GetCurrentObject Lib "gdi32" (ByVal hdc As Long, ByVal uObjectType As Long) As Long
Private Declare Function GetDIBits Lib "gdi32" (ByVal aHDC As Long, ByVal hBitmap As Long, ByVal nStartScan As Long, ByVal nNumScans As Long, lpBits As Any, lpBI As BitMapInfo, ByVal wUsage As Long) As Long

Private Type Font
    StartX As Integer
    StartY As Integer
    EndX As Integer
    EndY As Integer
End Type

Private Type multiRInfo
    multiIndex As Integer
    multiDX As Integer
    multiDY As Integer
    multiSX As Integer
    multiSY As Integer
    multiPower As Integer
    multiWaiting As Integer
    multiDirection As Integer '1 for X, 2 for Y
End Type

Private Type BitMapFileHeader
    bfType(0 To 1) As Byte
    bfSize As Long
    bfReserved1 As Integer
    bfReserved2 As Integer
    bfOffBits As Long
End Type

Private Type BitMapInfoHeader
   biSize As Long
   biWidth As Long
   biHeight As Long
   biPlanes As Integer
   biBitCount As Integer
   biCompression As Long
   biSizeImage As Long
   biXPelsPerMeter As Long
   biYPelsPerMeter As Long
   biClrUsed As Long
   biClrImportant As Long
End Type

Private Type RGBQuad
        rgbBlue As Byte
        rgbGreen As Byte
        rgbRed As Byte
        'rgbReserved As Byte
End Type

Private Type BitMapInfo
        bmiMHeader As BitMapFileHeader
        bmiHeader As BitMapInfoHeader
        'bmiColors As RGBQuad
End Type

Private Const Bits As Long = 32
Public Done As Boolean
Public TimeGet As Long
Public TimePut As Long
Dim ColVal() As Byte
Dim ColOut() As Byte
Dim InPutHei As Long
Dim InPutWid As Long
Dim PicInfo As BitMapInfo
Dim multiR() As multiRInfo













Private Sub AddtionDelayTime_Change()

    AddDelayTime = AddtionDelayTime.Text

End Sub







Private Sub Check1_Click()

    If Check1.Value = 1 Then
    
        'Command_Print_Pic.Visible = True
        StartDrawColor.Visible = True
        rastor_frame.Height = 3195
    
    Else
    
        'Command_Print_Pic.Visible = False
        StartDrawColor.Visible = False
        rastor_frame.Height = 2655
        'laser_power_frame.Height = 3500
    
    End If

End Sub




Private Sub Command_Multi_Rastor_Click()

    flagMultiRastor = True
    MultiRastor.Visible = True
    MoveStart.Visible = False
    MoveMultiRastor.Visible = True
    MultiRastor.Height = 3315
    MultiRastor.Left = 960
    MultiRastor.Top = 1800
    MultiRastor.Width = 5775
    rastor_frame.Height = 3195
    rastor_frame.Left = 1620
    rastor_frame.Top = 5160
    rastor_frame.Width = 4395

End Sub

Private Sub Command_close_multi_Click()

    flagMultiRastor = False
    MultiRastor.Visible = False
    MoveStart.Visible = True
    MoveMultiRastor.Visible = False
    If Check1.Value = 1 Then
        rastor_frame.Height = 3195
    Else
        rastor_frame.Height = 2655
    End If
    rastor_frame.Left = 1980
    rastor_frame.Top = 3240
    rastor_frame.Width = 3555

End Sub

Private Sub Command1_Click()
    
    StepFreq = laserMotorFreq * 8
    adjustLaser

End Sub



    
                








Private Sub Command2_Click()

    laserPosition = 0
    totalStep = 0
    CurrentAngle.Text = laserPosition
    Text3.Text = totalStep

End Sub











Private Sub Command5_Click()

    For i = 1 To 1000
        shutterOpen
        delayAccurate (100)
    Next

End Sub

Private Sub Command6_Click()

    sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        Dim ypic, Xpic As String
        
        ypic = Str(-150)
        Xpic = Str(0)
        lpic = Xpic + blank + ypic + blank + run + enter
        MSComm1.Output = lpic
        
        delayAccurate (500)
        If shutterIsOpen = True Then
            shutterClose
        Else
            shutterOpen
        End If
        delayAccurate (700)
        If shutterIsOpen = False Then
            shutterOpen
        Else
            shutterClose
        End If


End Sub

Private Sub Command7_Click()

    Dim Xpic, ypic As String

    sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent
        For i = 1 To 100
            ypic = Str(0.01)
            Xpic = Str(0)
            lpic = Xpic + blank + ypic + blank + run + enter
            MSComm1.Output = lpic
            delayAccurate (1 / Val(vel) * 10000 + 100)
        Next

End Sub

Private Sub Command8_Click()

    Advance_Pass.Visible = False

End Sub

Private Sub Command9_Click()

    Advance_Option.Visible = False

End Sub



'image handle, slow
'image handle, slow
'image handle, slow
'image handle, slow
'image handle, slow



'read RGB value, keep incase

'Private Sub input_pic_Click()
'
'    Dim picHandleX As Long
'    Dim picHandleY As Long
'    Dim r As Byte
'    Dim g As Byte
'    Dim b As Byte
'    Dim alpha As Byte
'    Dim width As Long
'    Dim height As Long
'    Dim currentPixel As Long
'    Dim pixelPannel() As Byte
'
'    currentPixel = 0
'
'    Open "E:\image\test1.bmp" For Binary As #1
'
'    Get #1, , PicInfo
'
'    width = Abs(PicInfo.bmiHeader.biWidth)
'    height = Abs(PicInfo.bmiHeader.biHeight)
'
'    ReDim pixelPannel(1 To 3, 1 To width, 1 To height)
'
'    'filelen = PicInfo.bmiHeader.biSizeImage
'    Text3.Text = "start"
'
'    For picHandleY = height To 1 Step -1
'
'        For picHandleX = 1 To width
'            currentPixel = currentPixel + 1
'            Get #1, , b
'            Get #1, , g
'            Get #1, , r
'            Get #1, , alpha
'            pixelPannel(3, picHandleX, picHandleY) = b
'            pixelPannel(2, picHandleX, picHandleY) = g
'            pixelPannel(1, picHandleX, picHandleY) = r
''            Text1.Text = b
''            Text3.Text = g
''            Text4.Text = r
''            Text5.Text = currentPixel
''            delay (1)
'        Next
'
'    Next
'    Text1.Text = currentPixel
'    Text3.Text = "end"
'
'    For picHandleY = 1 To height
'        For picHandleX = 1 To width
'            Text1.Text = pixelPannel(1, picHandleX, picHandleY)
'            Text3.Text = pixelPannel(2, picHandleX, picHandleY)
'            Text4.Text = pixelPannel(3, picHandleX, picHandleY)
'            Text5.Text = width * (picHandleY - 1) + picHandleX
'            delay (1)
'        Next
'    Next
'    Close #1
'
'End Sub



'convert to grey for drawing


Private Sub Command10_Click()

'    Open (App.Path & "\save\test.txt") For Input As #2
'    Dim testinput As c
'    Input #2, testinout
'    Input #2, testinput
'    Input #2, testinput
'    Text7.Text = testinput
'    Close #2
'    Dim i As Long
'    ReDim print_content(1 To Len(PrintContant.Text))
'    For i = 1 To UBound(print_content)
'        print_content(i) = Mid$(PrintContant.Text, i, 1)
'    Next
''    Dim text_length As Integer
''    text_length = Len(PrintContant.Text)
'
'    For i = 1 To UBound(print_content)
'        Select Case print_content(i)
'            Case "A"
'            Text7.Text = 12
'        End Select
'    Next
'
End Sub




Private Sub Drawpic_Load_Click()

    Dim tempStartValue As Integer
    Dim tempTime As Double
    Dim tempFilename As String
    Dim tempi As Integer
    Dim temp As Double
    Open (App.Path & "\save\DrawPic.inf") For Input As #2
    Input #2, tempFilename
    Input #2, tempStartValue
    Input #2, tempTime
    Input #2, temp
    velocity.Text = temp
    Input #2, temp
    DrawPicStepX.Text = temp
    Text20.Text = tempFilename
    Text14.Text = tempStartValue
    DrawPicStartValue = tempStartValue
    t = tempTime
    DrawPicPause.Caption = "Continue"
    flagDrawPicPause1 = True
    If shutterIsOpen = ture Then
        shutterClose
    End If
    
    input_pic_Click
    
    drawPicStatus.Cls
    drawPicStatus.FontSize = 8
    drawPicStatus.Align = 2
    drawPicStatus.Print "Drawing " & Text20.Text & ".bmp"
    
    DrawPicProgress.Cls
    DrawPicProgress.FontSize = 10
    For i = 1 To DrawPicStartValue / (picHeight / 34) - 1
            progressNum = progressNum + 1
            DrawPicProgress.Print "l";
    Next
    
    Close #2

End Sub

Private Sub Drawpic_Save_Click()

    If Text20.Text = "" Then
    Else
        Open (App.Path & "\save\DrawPic.inf") For Output As #3
        Write #3, Text20.Text
        Write #3, DrawPicStartValue
        Write #3, t
        Write #3, Val(velocity.Text)
        Write #3, Val(DrawPicStepX.Text)
        Close #3
    End If
    
End Sub

Private Sub DrawPicPause_Click()

    If drawing_mode = 1 Then
        If DrawPicPause.Caption = "Pause" Then
            DrawPicPause.Caption = "Continue"
            flagDrawPicPause1 = True
            If shutterIsOpen = ture Then
                shutterClose
            End If
            
        ElseIf DrawPicPause.Caption = "Continue" Then
            DrawPicPause.Caption = "Pause"
            flagDrawPicPause1 = False
            Timer1.Enabled = True
            If t > 60 Then
                flagSound = 1
            Else
                flagSound = 0
            End If
            drawRegion
        End If
    End If
End Sub

Private Sub Pic_mode1_Click()

    drawing_mode = 1

End Sub

Private Sub Pic_mode2_Click()

    drawing_mode = 2

End Sub

Private Sub Port_control_Click()

    If Port_control.Caption = "Close Port" Then
        Port_control.Caption = "Open Port"
        If MSComm1.PortOpen = True Then
            MSComm1.PortOpen = False
        End If
        Port_Warning.Visible = True
        Port_Warning.Cls
        Port_Warning.Print "    Warning: Port Closed"
    ElseIf Port_control.Caption = "Open Port" Then
        Port_control.Caption = "Close Port"
        If MSComm1.PortOpen = False Then
            MSComm1.PortOpen = True
        End If
        Port_Warning.Visible = False
    End If
    
End Sub




Private Sub StartPrint_Click()

    Dim i As Long
    ReDim print_content(1 To Len(PrintContant.Text))
    For i = 1 To UBound(print_content)
        print_content(i) = Mid$(PrintContant.Text, i, 1)
    Next
'    Dim text_length As Integer
'    text_length = Len(PrintContant.Text)
    
    For i = 1 To UBound(print_content)
        flagPrintEnd = False
    
        Select Case print_content(i)
            
            Case "a"
                Call drawFont(2, 1)
            Case "A"
                Call drawFont(4, 1)
                
            Case "b"
                Call drawFont(2, 2)
            Case "B"
                Call drawFont(4, 2)
            
            Case "c"
                Call drawFont(2, 3)
            Case "C"
                Call drawFont(4, 3)
            
            Case "d"
                Call drawFont(2, 4)
            Case "D"
                Call drawFont(4, 4)
            
            Case "e"
                Call drawFont(2, 5)
            Case "E"
                Call drawFont(4, 5)
                    
            Case "f"
                Call drawFont(2, 6)
            Case "F"
                Call drawFont(4, 6)
                    
            Case "g"
                Call drawFont(2, 7)
            Case "G"
                Call drawFont(4, 7)
                    
            Case "h"
                Call drawFont(2, 8)
            Case "H"
                Call drawFont(4, 8)
                    
            Case "i"
                Call drawFont(2, 9)
            Case "I"
                Call drawFont(4, 9)
                    
            Case "j"
                Call drawFont(2, 10)
            Case "J"
                Call drawFont(4, 10)
                    
            Case "k"
                Call drawFont(2, 11)
            Case "K"
                Call drawFont(4, 11)
                    
            Case "l"
                Call drawFont(2, 12)
            Case "L"
                Call drawFont(4, 12)
                    
            Case "m"
                Call drawFont(2, 13)
            Case "M"
                Call drawFont(4, 13)
                    
            Case "n"
                Call drawFont(3, 1)
            Case "N"
                Call drawFont(5, 1)
                
            Case "o"
                Call drawFont(3, 2)
            Case "O"
                Call drawFont(5, 2)
            
            Case "p"
                Call drawFont(3, 3)
            Case "P"
                Call drawFont(5, 3)
            
            Case "q"
                Call drawFont(3, 4)
            Case "Q"
                Call drawFont(5, 4)
            
            Case "r"
                Call drawFont(3, 5)
            Case "R"
                Call drawFont(5, 5)
                    
            Case "s"
                Call drawFont(3, 6)
            Case "S"
                Call drawFont(5, 6)
                    
            Case "t"
                Call drawFont(3, 7)
            Case "T"
                Call drawFont(5, 7)
                    
            Case "u"
                Call drawFont(3, 8)
            Case "U"
                Call drawFont(5, 8)
                    
            Case "v"
                Call drawFont(3, 9)
            Case "V"
                Call drawFont(5, 9)
                    
            Case "w"
                Call drawFont(3, 10)
            Case "W"
                Call drawFont(5, 10)
                    
            Case "x"
                Call drawFont(3, 11)
            Case "X"
                Call drawFont(5, 11)
                    
            Case "y"
                Call drawFont(3, 12)
            Case "Y"
                Call drawFont(5, 12)
                    
            Case "z"
                Call drawFont(3, 13)
            Case "Z"
                Call drawFont(5, 13)
                
            Case "0"
                Call drawFont(1, 10)
            Case "1"
                Call drawFont(1, 1)
            Case "2"
                Call drawFont(1, 2)
            Case "3"
                Call drawFont(1, 3)
            Case "4"
                Call drawFont(1, 4)
            Case "5"
                Call drawFont(1, 5)
            Case "6"
                Call drawFont(1, 6)
            Case "7"
                Call drawFont(1, 7)
            Case "8"
                Call drawFont(1, 8)
            Case "9"
                Call drawFont(1, 9)
            
            Case "-"
                Call drawFont(1, 11)
            Case "+"
                Call drawFont(1, 12)
            Case "."
                Call drawFont(1, 13)
'            Case 189
'                Call drawFont(1, 11)
'            Case 187
'                Call drawFont(1, 12)
'            Case 190
'                Call drawFont(1, 13)
            Case " "
                Call drawSpace
            
        End Select
        
        flagPrintEnd = True
    Next

End Sub

Private Sub drawSpace()

    Dim xspace As String
    Dim yspace As String
    
    yspace = Str(0)
    xspace = Str(10)
    
    lpic = xspace + blank + yspace + blank + run + enter
    MSComm1.Output = lpic
    delayAccurate (Val(xspace) / Val(vel) * 10000 + 200)

End Sub





Private Sub Text7_Change()
    
    'Text8.Text = s(Text7.Text)
    
End Sub

Private Sub input_pic_Click()

    drawPicStatus.Cls
    drawPicStatus.FontSize = 10
    drawPicStatus.Print "Inputing image"
    DrawPicProgress.Cls
    DrawPicProgress.FontSize = 10
    DrawPicProgress.Print "Please Wait"


    If Text20.Text = "" Then
    Else
        'Open (App.Path & "\image\drawthis.bmp") For Binary As #1
        Open (App.Path & "\image\" & Text20.Text & ".bmp") For Binary As #1
        
        input_picinfo
    End If
    
    
    
'            On Error GoTo err_handler
'
'err_handler:
'        Select Case Err.Number
'            Case 53:
'                MsgBox ("File Not Found")
'        End Select
    
End Sub


'Private Sub input_picinfo()
'
'    Dim picHandleX As Long
'    Dim picHandleY As Long
'    Dim r As Byte
'    Dim g As Byte
'    Dim b As Byte
'    Dim ri As Integer
'    Dim gi As Integer
'    Dim bi As Integer
'    Dim alpha As Byte
'    Dim currentPixel As Long
'    Dim iblank As Integer
'    Dim blanki As Integer
'    Dim progressNum As Integer
'    Dim progressDivide As Double
'
'    currentPixel = 0
'
'    DrawPicProgress.Cls
'    DrawPicProgress.FontSize = 12
'
'    Get #1, , PicInfo
'
'    'Text21.Text = PicInfo.bmiHeader.biBitCount
'    'Text21.Text = 3 Mod 4
'
'    picWidth = Abs(PicInfo.bmiHeader.biWidth)
'    picHeight = Abs(PicInfo.bmiHeader.biHeight)
'
'    If picWidth < 1 Then
'
'        MsgBox ("Wrong File Name")
'
'    Else
'
'        'ReDim pixelPannel(1 To picWidth, 1 To picHeight)
'
'
'        'filelen = PicInfo.bmiHeader.biSizeImage
'        ReDim newPixelPannel(1 To picWidth, 1 To (picHeight + 10))
'
'        progressNum = 1
'        progressDivide = (picHeight + 10) / 34
'
'        For picHandleY = picHeight + 10 To 1 Step -1
'
'            For picHandleX = 1 To picWidth
'                If picHandleY < 6 Then
'                    newPixelPannel(picHandleX, picHandleY) = 255
'                ElseIf picHandleY > picHeight + 5 Then
'                    newPixelPannel(picHandleX, picHandleY) = 255
'                Else
'                    currentPixel = currentPixel + 1
'                    Get #1, , b
'                    Get #1, , g
'                    Get #1, , r
'                    Get #1, , alpha
'                    ri = r
'                    gi = g
'                    bi = b
'                    newPixelPannel(picHandleX, picHandleY) = (ri + gi + bi) / 3
'                End If
'            Next
'
'            If picHandleY / progressDivide > progressNum Then
'                progressNum = progressNum + 1
'                DrawPicProgress.Print "l";
'            End If
'
'        Next
'
'
'
'
'        picHeight = picHeight + 10
'        drawPicStatus.Cls
'
'        'drawPicStatus.Print "   Completed"
'        drawPicStatus.Print " " & Text20.Text & ".bmp"
'
'    '        DrawPicProgress.Cls
'    '        DrawPicProgress.FontSize = 12
'    '        DrawPicProgress.Print "lllllllllllllllllllllllllllllllll"
'
'    End If
'
'    Close #1
'
'End Sub



Private Sub input_picinfo()

    Dim picHandleX As Long
    Dim picHandleY As Long
    Dim r As Byte
    Dim g As Byte
    Dim b As Byte
    Dim ri As Integer
    Dim gi As Integer
    Dim bi As Integer
    Dim alpha As Byte
    Dim currentPixel As Long
    Dim iblank As Integer
    Dim blanki As Integer
    currentPixel = 0



    Get #1, , PicInfo

    'Text21.Text = PicInfo.bmiHeader.biBitCount
    'Text21.Text = 3 Mod 4

    picWidth = Abs(PicInfo.bmiHeader.biWidth)
    picHeight = Abs(PicInfo.bmiHeader.biHeight)

    If picWidth < 1 Then

        MsgBox ("Wrong File Name")

    Else

        ReDim pixelPannel(1 To picWidth, 1 To picHeight)


        'filelen = PicInfo.bmiHeader.biSizeImage

        If PicInfo.bmiHeader.biBitCount = 32 Then

            For picHandleY = picHeight To 1 Step -1

                For picHandleX = 1 To picWidth
                    currentPixel = currentPixel + 1
                    Get #1, , b
                    Get #1, , g
                    Get #1, , r
                    Get #1, , alpha
                    ri = r
                    gi = g
                    bi = b
                    pixelPannel(picHandleX, picHandleY) = (ri + gi + bi) / 3
        '            newPixelPannel(2 * picHandleX - 1, 2 * picHandleY - 1) = (ri + gi + bi) / 3
        '            newPixelPannel(2 * picHandleX - 1, 2 * picHandleY) = (ri + gi + bi) / 3
        '            newPixelPannel(2 * picHandleX, 2 * picHandleY - 1) = (ri + gi + bi) / 3
        '            newPixelPannel(2 * picHandleX, 2 * picHandleY) = (ri + gi + bi) / 3
                Next

            Next

        ElseIf PicInfo.bmiHeader.biBitCount = 24 Then

            iblank = (picWidth * 3) Mod 4
            iblank = 4 - iblank
            If iblank = 4 Then
                iblank = 0
            End If

            For picHandleY = picHeight To 1 Step -1

                For picHandleX = 1 To picWidth
                    currentPixel = currentPixel + 1
                    Get #1, , b
                    Get #1, , g
                    Get #1, , r
                    ri = r
                    gi = g
                    bi = b
                    pixelPannel(picHandleX, picHandleY) = (ri + gi + bi) / 3

                Next

                For blanki = 1 To iblank
                    Get #1, , alpha
                Next

            Next
        Else
            MsgBox ("Wrong Picture Format")
        End If

        ReDim newPixelPannel(1 To picWidth, 1 To (picHeight + 10))

        For picHandleX = 1 To picWidth
            For picHandleY = 1 To 5
                newPixelPannel(picHandleX, picHandleY) = 255
            Next
            For picHandleY = 6 To (5 + picHeight)
                newPixelPannel(picHandleX, picHandleY) = pixelPannel(picHandleX, picHandleY - 5)
            Next
            For picHandleY = (6 + picHeight) To (10 + picHeight)
                newPixelPannel(picHandleX, picHandleY) = 255
            Next
        Next

        picHeight = picHeight + 10
        drawPicStatus.Cls

        'drawPicStatus.Print "   Completed"
        drawPicStatus.Print " " & Text20.Text & ".bmp"

        DrawPicProgress.Cls
'        DrawPicProgress.FontSize = 12
'        DrawPicProgress.Print "lllllllllllllllllllllllllllllllll"

    End If

    Close #1

End Sub



Private Sub Command3_Click()

    Dim testStageX As String
    Dim testStageY As String
    Dim testStageY1 As String
    Dim teststageNX As String
    Dim teststageNY As String
    Dim teststageNY1 As String
    testStageX = Str(1)
    testStageY = Str(500)
    teststageNY = Str(-500)
    testStageY1 = Str(2)
    teststageNY1 = Str(-2)
    Dim watch As Double
    
    Dim thisi As Integer
    Dim thisj As Integer
    
     sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
    ltestx = testStageX + blank + Str(0) + blank + run + enter
    ltesty = Str(0) + blank + testStageY + blank + run + enter
    ltestny = Str(0) + blank + teststageNY + blank + run + enter
    ltesty1 = Str(0) + blank + testStageY1 + blank + run + enter
    ltestny1 = Str(0) + blank + teststageNY1 + blank + run + enter
            
        For thisi = 1 To 100
            For thisj = 1 To 1
                MSComm1.Output = ltesty
                delayAccurate (Val(testStageY) * 10000 / Val(vel) + 400)
'                watch = testStageY * 10000 / Val(vel)
'                'delay (0.1)
'                MSComm1.Output = ltesty1
'                delayAccurate (Val(testStageY1) * 10000 / Val(vel) + 400)
'                watch = testStageY1 * 10000 / Val(vel)
'                'delay (0.1)
            Next
            MSComm1.Output = ltestx
            delayAccurate (Val(testStageX) * 10000 / Val(vel) + 400)
'            watch = testStageX * 10000 / Val(vel)
            'delay (1)
            For thisj = 1 To 1
                MSComm1.Output = ltestny
                delayAccurate (Val(testStageY) * 10000 / Val(vel) + 400)
'                watch = testStageY * 10000 / Val(vel)
'                'delay (0.1)
'                MSComm1.Output = ltestny1
'                delayAccurate (Val(testStageY1) * 10000 / Val(vel) + 400)
'                watch = testStageY * 10000 / Val(vel)
'                'delay (0.1)
            Next
            MSComm1.Output = ltestx
            delayAccurate (Val(testStageX) * 10000 / Val(vel) + 400)
'            watch = testStageY * 10000 / Val(vel)
            'delay (1)
        Next

End Sub










Private Sub Option1_Click()

    flagPrintMode = 1

End Sub

Private Sub Option2_Click()

    flagPrintMode = 2

End Sub



Private Sub MoveMultiRastor_Click()

    MoveMultiRastorFun

End Sub

Private Sub MultiRastorDirection_Click()

    If flagMultiDirection = 1 Then
        flagMultiOrder = 2
        MultiRastorOrder.Caption = "No. of Suqares/Col:"
        flagMultiDirection = 2
        MultiRastorDirection.Caption = "Y"
    ElseIf flagMultiDirection = 2 Then
        flagMultiOrder = 1
        MultiRastorOrder.Caption = "No. of Suqares/Row:"
        flagMultiDirection = 1
        MultiRastorDirection.Caption = "X"
    End If

End Sub

Private Sub MultiRastorOrder_Click()

    If flagMultiOrder = 1 Then
        flagMultiOrder = 2
        MultiRastorOrder.Caption = "No. of Suqares/Col:"
        flagMultiDirection = 2
        MultiRastorDirection.Caption = "Y"
    ElseIf flagMultiOrder = 2 Then
        flagMultiOrder = 1
        MultiRastorOrder.Caption = "No. of Suqares/Row:"
        flagMultiDirection = 1
        MultiRastorDirection.Caption = "X"
    End If

End Sub

Private Sub Option_PrintTpye1_Click()

    printType1 = True
    printType2 = False
    If FontChoice.Text = "Choose Font" Then
        Open (App.Path & "\font\TimesNewRoman.font") For Binary As #1
        input_FontPixel
        input_FontLocation
        FontChoice.Text = "Times New Roman"
    End If
    StartPrint.Visible = False

End Sub

Private Sub Option_PrintType2_Click()

    printType1 = False
    printType2 = True
    If FontChoice.Text = "Choose Font" Then
        Open (App.Path & "\font\TimesNewRoman.font") For Binary As #1
        input_FontPixel
        input_FontLocation
        FontChoice.Text = "Times New Roman"
    End If
    StartPrint.Visible = True

End Sub

Private Sub SetCor_Click()

    positionX = CorXV.Text
    positionY = CorYV.Text
    If flagDisStage = 1 Then
        WorldX = CorXV.Text
        WorldY = CorYV.Text
    ElseIf flagDisStage = 0 Then
        WorldX = -1 * CorXV.Text
        WorldY = -1 * CorYV.Text
    End If
    
    arrowXpic.Cls
    
    arrowXpic.Cls
    
    arrowXpic.ForeColor = &HFF00&
    
    arrowXpic.Print positionX
    
    CorXV = positionX
    
    
    arrowYpic.Cls

    arrowYpic.ForeColor = &HFF00&

    arrowYpic.Print positionY
    
    CorYV = positionY

End Sub

Private Sub RunToCor_Click()


        sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
        
        flagFirst = 0
        sent = vel + "setvel" + enter
        
        
        
        Dim tempUseX, tempUseY As Integer
        
        If flagDisStage = 1 Then
            tempUseX = -1 * CorXV
            tempUseY = -1 * CorYV
        ElseIf flagDisStage = 0 Then
            tempUseX = CorXV
            tempUseY = CorYV
        End If
        
        
        Dim tempRunX, tempRunY As String
        Dim tempTime As Double
        Dim actualVel As String
        
        tempRunX = Str(tempUseX + WorldX)
        tempRunY = Str(tempUseY + WorldY)
        
        If (Abs(Val(tempRunX)) + Abs(Val(tempRunY))) > 0 Then
            If Abs(Val(tempRunX)) > Abs(Val(tempRunY)) Then
                tempTime = (Abs(Val(tempRunX) ^ 2) + Abs(Val(tempRunY) ^ 2)) ^ (1 / 2) / Val(vel)
                actualVel = Str(Abs(Val(tempRunX)) / tempTime)
            Else
                tempTime = (Abs(Val(tempRunX) ^ 2) + Abs(Val(tempRunY) ^ 2)) ^ (1 / 2) / Val(vel)
                actualVel = Str(Abs(Val(tempRunY)) / tempTime)
            End If
            
            sentav = actualVel + "setvel" + enter
            
            temprun = tempRunX + blank + tempRunY + blank + run + enter
            MSComm1.Output = sentav
            MSComm1.Output = temprun
            
            Debug.Print sent
            MSComm1.Output = sent
            
            positionX = CorXV.Text
            positionY = CorYV.Text
            If flagDisStage = 1 Then
                WorldX = CorXV.Text
                WorldY = CorYV.Text
            ElseIf flagDisStage = 0 Then
                WorldX = -1 * CorXV.Text
                WorldY = -1 * CorYV.Text
            End If
            
            arrowXpic.Cls
            
            arrowXpic.Cls
            
            arrowXpic.ForeColor = &HFF&
            
            arrowXpic.Print positionX
            
            CorXV = positionX
            
            
            arrowYpic.Cls
        
            arrowYpic.ForeColor = &HFF&
        
            arrowYpic.Print positionY
            
            CorYV = positionY
            
            delay (tempTime)
    
            SetCor_Click
        End If
End Sub

Private Sub SetMultiRastorParameters_Click()

    totalMultiNum = MultiSquareNumber.Text
    ReDim multiR(1 To totalMultiNum)
    Dim multiI As Integer
    Dim lowPower, highPower As Integer
    lowPower = MultiRastorStartPower
    highPower = MultiRastorEndPower
    For multiI = 1 To totalMultiNum
        multiR(multiI).multiDirection = flagMultiDirection
        multiR(multiI).multiDX = SquareDimensionX.Text
        multiR(multiI).multiDY = SquareDimensionY.Text
        multiR(multiI).multiIndex = multiI
        multiR(multiI).multiSX = MultiRastorRowSpacing.Text
        multiR(multiI).multiSY = MultiRastorColSpacing.Text
        multiR(multiI).multiWaiting = MultiRastorWaiting.Text
        multiR(multiI).multiPower = lowPower + (multiI - 1) * (highPower - lowPower) / (totalMultiNum - 1)
    Next

End Sub

Private Sub ShutterOffTimeValue_Change()

    ShutterControlOffTime = ShutterOffTimeValue.Text

End Sub

Private Sub shutterControlOperate_Click()

    Dim shutterControli As Integer
    If shutterIsOpen = True Then
            shutterClose
    End If
    ypic.Cls
        
    ypic.Print "Preparing"
    delayAccurate (2 * 10000)
    For shutterControli = 1 To shutterControlLoop
    
        ypic.Cls
        
        ypic.Print shutterControli
        
        If shutterIsOpen = False Then
            'shutterOpen
            Laser_Open_Click
        End If
        delayAccurate (ShutterControlOnTime * 10000)
        
        If shutterIsOpen = True Then
            'shutterClose
            Laser_Close_Click
        End If
        delayAccurate (ShutterControlOffTime * 10000)

    Next
    
    If shutterIsOpen = True Then
        shutterClose
    End If

End Sub

Private Sub ShutterLoopValue_Change()
    
    shutterControlLoop = ShutterLoopValue.Text
    
End Sub

Private Sub ShutterOnTimeValue_Change()
    
    ShutterControlOnTime = ShutterOnTimeValue.Text
    
End Sub



Private Sub StartDraw_Click()

    picRegionMax = Val(DrawPicMax.Text)
    picRegionMin = Val(DrawPicMin.Text)
    flagDrawPicPause1 = False
    flagDrawpicAbort1 = False
    DrawPicStartValue = 1

    If drawing_mode = 1 Then
        
        
        DrawPicTime1 = 0
        
        
        drawPicStatus.Cls
        drawPicStatus.FontSize = 10
        drawPicStatus.Print "CalculatingTime"
        
        calDrawRegion
        
        drawPicStatus.Cls
        drawPicStatus.FontSize = 8
        drawPicStatus.Align = 2
        drawPicStatus.Print "Drawing " & Text20.Text & ".bmp"
        
        t = DrawPicTime1 / 10000
        Timer1.Enabled = True
        If t > 60 Then
            flagSound = 1
        Else
            flagSound = 0
        End If
        
        Text14.Text = 1
        
        drawRegion
    
    ElseIf drawing_mode = 2 Then
    
        drawRegion2
    
    End If

End Sub

'Public Sub countnum()
'
'    If drawLength = 2 Then
'        Text5.Text = Text5.Text + 1
'    End If
'    If drawLength = 3 Then
'        Text6.Text = Text6.Text + 1
'    End If
'    If drawLength = 4 Then
'        Text7.Text = Text7.Text + 1
'    End If
'    If drawLength = 5 Then
'        Text8.Text = Text8.Text + 1
'    End If
'    If drawLength = 6 Then
'        Text9.Text = Text9.Text + 1
'    End If
'    If drawLength = 1 Then
'        Text10.Text = Text10.Text + 1
'    End If
'
'
'
'End Sub

Private Sub StartDrawColor_Click()
    Dim thisi As Integer
    Dim storePower(1 To 5) As Integer
    Dim picCorrect(1 To 5) As Integer
    Dim resetThisX, resetThisY As String
    '850
    storePower(1) = 865
    picCorrect(1) = 130
    storePower(2) = 750
    picCorrect(2) = 130
    storePower(3) = 845
    picCorrect(3) = 130
    storePower(4) = 810
    picCorrect(4) = 130
    storePower(5) = 800
    picCorrect(5) = 130
    
    
    
    'If picWidth Mod 2 = 1 Then
    '    resetThisX = Str(-picWidth)
    '    resetThisY = Str(picHeight)
    'ElseIf picWidth Mod 2 = 0 Then
    '    resetThisX = Str(-picWidth)
    '    resetThisY = Str(0)
    'End If
    
    sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent


        
    
    
    For thisi = 1 To 1
    
'        picRegionMax = thisi * 60
'        picRegionMin = (thisi - 1) * 60 - 1
        picRegionMax = 200
        picRegionMin = 100
        picDrawCorrect = picCorrect(thisi)
        If shutterIsOpen = True Then
            shutterClose
        End If
        goToStepNum = 0
        adjustLaser
        
        delay (60)
'        If thisi > 1 Then
'            resetThisX = Str(-1 * CorXV.Text + 5)
'            resetThisY = Str(-1 * CorYV.Text)
'            CorXV.Text = CorXV.Text - CorXV.Text
'            CorYV.Text = CorYV.Text - CorYV.Text
'            lreset = resetThisX + blank + resetThisY + blank + run + enter
'            MSComm1.Output = lreset
'        End If
        goToStepNum = storePower(thisi)
        adjustLaser
        delay (60)
        drawRegion
    
    Next
    

End Sub


Public Sub adjustLaser()

    StepFreq = 1000 * 8

    changeStep = goToStepNum - totalStep
    
    If changeStep > 0 Then
        changeStep = changeStep * 8
        For i = 1 To changeStep
            out Val("&H378"), Val(100)
            delayAccurate (1 / StepFreq * 10000)
            out Val("&H378"), Val(0)
            delayAccurate (1 / StepFreq * 10000)
        Next
        
        laserPosition = laserPosition + changeStep * 1.8 / 8
        totalStep = totalStep + changeStep / 8
        CurrentAngle.Text = laserPosition
        Text3.Text = totalStep
    ElseIf changeStep < 0 Then
    
        changeStep = -1 * changeStep * 8
            
        
        For i = 1 To changeStep
            out Val("&H378"), Val(1100)
            delayAccurate (1 / StepFreq * 10000)
            out Val("&H378"), Val(1000)
            delayAccurate (1 / StepFreq * 10000)
        Next
        laserPosition = laserPosition - changeStep * 1.8 / 8
        totalStep = totalStep - changeStep / 8
        CurrentAngle.Text = laserPosition
        Text3.Text = totalStep
    
    End If

End Sub





Public Sub drawRegion2()

    Dim picDrawX As Integer
    Dim picDrawY As Integer
    Dim startValue As Integer
    Dim endValue As Integer
    Dim sameRegion As Boolean
    Dim drawLength As Integer
    Dim haveColorPre As Boolean
    Dim haveColorNow As Boolean
    Dim iniP As Boolean
    Dim Xpic, ypic As String
    Dim flagExtra As Boolean
    Dim timeDelayed As Long

    Dim StepSizeX As Double
    StepSizeX = DrawPicStepX.Text
    
    timeDelayed = 0
    flagExtra = False


        sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent


'        lpic = Xpic + blank + Ypic + blank + run + enter
        ypic = Str(-picHeight - 10 - DrawPicExtraBoundry)
        lYpic = Str(0) + blank + ypic + blank + run + enter
    
    If newPixelPannel(1, 1) < picRegionMax Then
        If newPixelPannel(1, 1) > picRegionMin Then
            haveColorPre = True
        End If
'    ElseIf newpixelpannel(1, 1) > picRegionWhite Then
    Else
        haveColorPre = False
    End If
    
    
    'picTimeStep 1->have color    2->no color
    
    If shutterIsOpen = True Then
        shutterClose
    End If
    
    picHeight = picHeight + 10
    
    For picDrawX = 1 To picWidth
                        
            timeNum = 1
            delay (1)
            timeDelayed = 0
            sent = vel + "setvel" + enter
            Debug.Print sent
            MSComm1.Output = sent
            ypic = Str(-picHeight - 10 - DrawPicExtraBoundry - Val(vel))
            lYpic = Str(0) + blank + ypic + blank + run + enter
            MSComm1.Output = lYpic
            
            delayAccurate (10000)
            timeDelayed = timeDelayed + 10000
            For picDrawY = 1 To picHeight
            
                If newPixelPannel(picDrawX, picDrawY) < picRegionMax Then
                    If newPixelPannel(picDrawX, picDrawY) > picRegionMin Then
                        haveColorNow = True
                    End If
'                ElseIf newpixelpannel(picDrawX, picDrawY) > picRegionWhite Then
                Else
                    haveColorNow = False
                End If
                
                If haveColorNow = haveColorPre Then
                    sameRegion = True
                Else
                    sameRegion = False
                End If
                

                If picDrawY = 1 Then
                    startValue = 1
                End If
                
                If picDrawY < picHeight Then
                
                    If sameRegion = False Then
                        drawLength = picDrawY - startValue
                        
                        If haveColorPre = True Then
                        
                            If shutterIsOpen = False Then
                                shutterOpen
                            End If
                            
                            delayAccurate (drawLength / Val(vel) * 10000)
                            timeDelayed = timeDelayed + drawLength / Val(vel) * 10000
                            If drawLength / Val(vel) * 10000 = 0 Then
                                Text5.Text = 11111
                            End If
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                        
                            
                        ElseIf haveColorPre = False Then
                            
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            delayAccurate (drawLength / Val(vel) * 10000)
                            timeDelayed = timeDelayed + drawLength / Val(vel) * 10000
                            If drawLength / Val(vel) * 10000 = 0 Then
                                Text5.Text = 11111
                            End If
'                            If shutterIsOpen = False Then
'                                shutterOpen
'                            End If
                        End If
                            
                        startValue = picDrawY
                            
                    End If
                
                
                ElseIf picDrawY = picHeight Then
                    If sameRegion = True Then
                        If haveColorNow = True Then
                        
                            drawLength = picHeight - startValue + 1
                            If shutterIsOpen = False Then
                                shutterOpen
                            End If
                            delayAccurate (drawLength / Val(vel) * 10000)
                            timeDelayed = timeDelayed + drawLength / Val(vel) * 10000
                            If drawLength / Val(vel) * 10000 = 0 Then
                                Text5.Text = 11111
                            End If
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                        
                        ElseIf haveColorNow = False Then
                        
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            
                            drawLength = picHeight + 1 - startValue
                            delayAccurate (drawLength / Val(vel) * 10000)
                            If drawLength / Val(vel) * 10000 = 0 Then
                                Text5.Text = 11111
                            End If
                            timeDelayed = timeDelayed + drawLength / Val(vel) * 10000
                            
'                            If shutterIsOpen = False Then
'                                shutterOpen
'                            End If

                        
                        End If
                    
                    End If
                
                    timeDelayed = ((picHeight + 10 + DrawPicExtraBoundry + Val(vel)) / Val(vel) * 10000 + 400) - timeDelayed
                    delayAccurate (timeDelayed)
                    
                    If shutterIsOpen = True Then
                        shutterClose
                    End If
                    Xpic = Str(StepSizeX)
                    
                    lpic = Xpic + blank + Str(0) + blank + run + enter
                    MSComm1.Output = lpic
                    CorXV.Text = CorXV.Text + 1
                    Text1.Text = "x+1"
                    delayAccurate (StepSizeX / Val(vel) * 10000 + 400)
                    delay (0.05)
                    
                    
                    sent = Str(1000) + "setvel" + enter
                    Debug.Print sent
                    MSComm1.Output = sent
                    ypic = Str(picHeight + 10 + DrawPicExtraBoundry + Val(vel))
                    lpic = Str(0) + blank + ypic + blank + run + enter
                    MSComm1.Output = lpic
                    delayAccurate ((picHeight + 10 + DrawPicExtraBoundry + Val(vel)) / 1000 * 10000 + 500)
                    
                    If picDrawX < picWidth Then
                    
                        If newPixelPannel(picDrawX + 1, 1) < picRegionMax Then
                            If newPixelPannel(picDrawX + 1, 1) > picRegionMin Then
                                haveColorNow = True
                            End If
                        
                        ElseIf newPixelPannel(picDrawX + 1, picHeight) > picRegionMin Then
                        Else
                            haveColorNow = False
                        End If
                        
                    End If
                    
                End If
                
                haveColorPre = haveColorNow
      
            Next
            

    Next

End Sub






Public Sub drawRegion()

        Dim picDrawX As Integer
    Dim picDrawY As Integer
    Dim startValue As Integer
    Dim endValue As Integer
    Dim sameRegion As Boolean

    Dim haveColorPre As Boolean
    Dim haveColorNow As Boolean
    Dim iniP As Boolean
    Dim Xpic, ypic As String
    Dim flagExtra As Boolean
    Dim countCorrect As Integer
    Dim StepSizeX As Double
    StepSizeX = DrawPicStepX.Text
    'Dim flagCorrect As bollean
    
    
    Dim progressNum As Integer
    Dim progressDivide As Double
    
    progressDivide = picWidth / 34
    progressNum = DrawPicStartValue \ progressDivide + 1

    picDrawCorrect = 100000
    countCorrect = 0
    testCorrection = 2
    'flagCorrect = False

    flagExtra = False


        sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent


'        lpic = Xpic + blank + Ypic + blank + run + enter

'    picRegionMin = -1
'    picRegionMax = 200
    
    If newPixelPannel(DrawPicStartValue, 1) < picRegionMax Then
        If newPixelPannel(DrawPicStartValue, 1) > picRegionMin Then
            haveColorPre = True
        End If
'       ElseIf newpixelpannel(1, 1) > picRegionWhite Then
        Else
            haveColorPre = False
        End If
    
    If shutterIsOpen = True Then
        shutterClose
    End If
    
'    ypic = Str(-10)
'    Xpic = Str(0)
'    lpic = Xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(ypic) / Val(vel)) * 10000 + 1000)
'
'    ypic = Str(0)
'    Xpic = Str(-10)
'    lpic = Xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(Xpic) / Val(vel)) * 10000 + 1000)
'
'    ypic = Str(10)
'    Xpic = Str(0)
'    lpic = Xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(ypic) / Val(vel)) * 10000 + 1000)
'
'    ypic = Str(0)
'    Xpic = Str(10)
'    lpic = Xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(Xpic) / Val(vel)) * 10000 + 1000)
    
    
    
    For picDrawX = DrawPicStartValue To picWidth
    
        If flagDrawPicPause1 = False Then
    
            If picDrawX Mod 2 = 1 Then
            
            ypic = Str(testCorrection * -1)
            Xpic = Str(0)
            lpic = Xpic + blank + ypic + blank + run + enter
            MSComm1.Output = lpic
            delayAccurate (Abs(Val(Xpic) / Val(vel)) * 10000 + 1000)
            
                For picDrawY = 1 To picHeight
                    
                    haveColorNow = False
                    If newPixelPannel(picDrawX, picDrawY) < picRegionMax Then
                        If newPixelPannel(picDrawX, picDrawY) > picRegionMin Then
                            haveColorNow = True
                        Else
                            haveColorNow = False
                        End If
    '                ElseIf newpixelpannel(picDrawX, picDrawY) > picRegionWhite Then
                    Else
                        haveColorNow = False
                    End If
                    
                    If haveColorNow = haveColorPre Then
                        sameRegion = True
                    Else
                        sameRegion = False
                    End If
                    
    
                    If picDrawY = 1 Then
                        startValue = 1
                    End If
                    
                    If picDrawY < picHeight Then
                    
                        If sameRegion = False Then
                            drawLength = picDrawY - startValue
                            
                            If haveColorPre = True Then
                            
                                drawLength = drawLength - 1
    '                            If startValue = 1 Then
    '                                drawLength = drawLength + 1
    '                            End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
    
                                If drawLength > 0 Then
                                    delayAccurate (1 / Val(vel) * 10000)
                                    ypic = Str(-1 * drawLength)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    'countnum
                                    CorYV.Text = CorYV.Text - drawLength
                                    Text1.Text = "y-" & drawLength
                                    delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                    delayAccurate (1 / Val(vel) * 10000)
                                    
                                    countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
                                ElseIf drawLength = 0 Then
                                    delayAccurate (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                
                            ElseIf haveColorPre = False Then
                                
                                If startValue = 1 Then
                                    drawLength = drawLength
                                Else
                                    drawLength = drawLength + 1
                                End If
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                ypic = Str(-1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text - drawLength
                                Text1.Text = "y-" & drawLength
                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                            End If
                                
                            startValue = picDrawY
                                
                        End If
                    
                    
                    ElseIf picDrawY = picHeight Then
                        If sameRegion = True Then
                            If haveColorNow = True Then
                            
                                drawLength = picHeight - startValue
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If drawLength > 0 Then
                                   delayAccurate (1 / Val(vel) * 10000)
                                   ypic = Str(-1 * drawLength)
                                   Xpic = Str(0)
                                   lpic = Xpic + blank + ypic + blank + run + enter
                                   MSComm1.Output = lpic
                                   'countnum
                                   CorYV.Text = CorYV.Text - drawLength
                                   Text1.Text = "y-" & drawLength
                                   delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                   delayAccurate (1 / Val(vel) * 10000)
                                   
                                   countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                                ElseIf drawLength = 0 Then
                                    delayAccurate (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                            
                            ElseIf haveColorNow = False Then
                            
                                drawLength = picHeight + 1 - startValue
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                ypic = Str(-1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text - drawLength
                                Text1.Text = "y-" & drawLength
                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                            
                            End If
                        
    '                    ElseIf sameRegion = False Then
    '
    '                        drawLength = picDrawY - startValue
    '                        startValue = picDrawY
    '                        If haveColorPre = True Then
    '
    '                            drawLength = drawLength - 1
    '                            If shutterIsOpen = False Then
    '                                shutterOpen
    '                            End If
    '                            If drawLength = 1 Then
    '                                drawLength = 0
    '                                flagExtra = True
    '                            End If
    '                            If drawLength > 0 Then
    '                                delayAccurate (1 / Val(vel) * 10000)
    '                                ypic = Str(-1 * drawLength)
    '                                Xpic = Str(0)
    '                                lpic = Xpic + blank + ypic + blank + run + enter
    '                                MSComm1.Output = lpic
    '                                CorYV.Text = CorYV.Text - drawLength
    '                                Text1.Text = "y-" & drawLength
    '                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
    '                                delayAccurate (1 / Val(vel) * 10000)
    '                            ElseIf drawLength = 0 Then
    '                                delayAccurate (1 / Val(vel) * 10000 + 200)
    '                            End If
    '
    '                            If shutterIsOpen = True Then
    '                                shutterClose
    '                            End If
    '
    '                        ElseIf haveColorPre = False Then
    '
    '
    '                            drawLength = drawLength + 1
    '                            If flagExtra = True Then
    '                                drawLength = drawLength + 1
    '                                flagExtra = False
    '                            End If
    '                            If shutterIsOpen = True Then
    '                                shutterClose
    '                            End If
    '                            ypic = Str(-1 * drawLength)
    '                            Xpic = Str(0)
    '                            lpic = Xpic + blank + ypic + blank + run + enter
    '                            MSComm1.Output = lpic
    '                            CorYV.Text = CorYV.Text - drawLength
    '                            Text1.Text = "y-" & drawLength
    '                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
    '                        End If
    '
    '                        If haveColorNow = True Then
    '
    '                            If shutterIsOpen = False Then
    '                                shutterOpen
    '                            End If
    '
    '                            delayAccurate (1 / Val(vel) * 10000 + 200)
    '
    '                        ElseIf haveColorNow = False Then
    '
    '                            If shutterIsOpen = True Then
    '                                shutterClose
    '                            End If
    '
    '                            drawLength = 1
    '                            If flagExtra = True Then
    '                                drawLength = drawLength + 1
    '                                flagExtra = False
    '                            End If
    '                            ypic = Str(-1 * drawLength)
    '                            Xpic = Str(0)
    '                            lpic = Xpic + blank + ypic + blank + run + enter
    '                            MSComm1.Output = lpic
    '                            CorYV.Text = CorYV.Text - drawLength
    '                            Text1.Text = "y-" & drawLength
    '                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
    '
    '                        End If
                        
                        End If
                        
    
    
            
                    
                        
                        If shutterIsOpen = True Then
                            shutterClose
                        End If
                        ypic = Str(0)
                        Xpic = Str(StepSizeX)
                        
                        lpic = Xpic + blank + ypic + blank + run + enter
                        MSComm1.Output = lpic
                        CorXV.Text = CorXV.Text + 1
                        Text14.Text = Text14.Text + 1
                        delayAccurate (2 * StepSizeX / Val(vel) * 10000 + 200)
                        
                        If picDrawX < picWidth Then
                        
                            If newPixelPannel(picDrawX + 1, picHeight) < picRegionMax Then
                                If newPixelPannel(picDrawX + 1, picHeight) > picRegionMin Then
                                    haveColorNow = True
                                End If
                            
    '                        ElseIf newpixelpannel(picDrawX + 1, picHeight) > picRegionMin Then
                            Else
                                haveColorNow = False
                            End If
                            
                        End If
                        
                    End If
                    
                    haveColorPre = haveColorNow
          
                Next
                
            ElseIf picDrawX Mod 2 = 0 Then
            
            ypic = Str(testCorrection)
            Xpic = Str(0)
            lpic = Xpic + blank + ypic + blank + run + enter
            MSComm1.Output = lpic
            delayAccurate (Abs(Val(Xpic) / Val(vel)) * 10000 + 100)
            
                For picDrawY = picHeight To 1 Step -1
                    haveColorNow = False
                    If newPixelPannel(picDrawX, picDrawY) < picRegionMax Then
                        If newPixelPannel(picDrawX, picDrawY) > picRegionMin Then
                            haveColorNow = True
                        Else
                            haveColorNow = False
                        End If
    '                ElseIf newpixelpannel(picDrawX, picDrawY) > picRegionMin Then
                    Else
                        haveColorNow = False
                    End If
                    
                    If haveColorNow = haveColorPre Then
                        sameRegion = True
                    Else
                        sameRegion = False
                    End If
                    
    
                    If picDrawY = picHeight Then
                        startValue = picHeight
                    End If
                    
                    If picDrawY > 1 Then
                    
                        If sameRegion = False Then
                            drawLength = startValue - picDrawY
                            
                            If haveColorPre = True Then
                            
                                drawLength = drawLength - 1
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If drawLength > 0 Then
                                    delayAccurate (1 / Val(vel) * 10000)
                                    ypic = Str(1 * drawLength)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    'countnum
                                    CorYV.Text = CorYV.Text + drawLength
                                    Text1.Text = "y" & drawLength
                                    delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                    delayAccurate (1 / Val(vel) * 10000)
                                    
                                    countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                                ElseIf drawLength = 0 Then
                                    delayAccurate (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                
                            ElseIf haveColorPre = False Then
                                    
                                If startValue = picHeight Then
                                    drawLength = drawLength
                                Else
                                    drawLength = drawLength + 1
                                End If
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                ypic = Str(1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text + drawLength
                                Text1.Text = "y" & drawLength
                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                            End If
                            startValue = picDrawY
                        End If
                    
                    
                    ElseIf picDrawY = 1 Then
                        If sameRegion = True Then
                            If haveColorNow = True Then
                            
                                drawLength = startValue - 1
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If drawLength > 0 Then
                                   delayAccurate (1 / Val(vel) * 10000)
                                   ypic = Str(1 * drawLength)
                                   Xpic = Str(0)
                                   lpic = Xpic + blank + ypic + blank + run + enter
                                   MSComm1.Output = lpic
                                   'countnum
                                   CorYV.Text = CorYV.Text + drawLength
                                   Text1.Text = "y" & drawLength
                                   delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                   delayAccurate (1 / Val(vel) * 10000)
                                   
                                   countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                                ElseIf drawLength = 0 Then
                                    delayAccurate (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                            
                            ElseIf haveColorNow = False Then
    
                                drawLength = startValue - 1 + 1
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                ypic = Str(1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text + drawLength
                                Text1.Text = "y" & drawLength
                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        MSComm1.Output = lpic
                                        delayAccurate (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
    
                            End If
    '
    '                    ElseIf sameRegion = False Then
    '
    '                        drawLength = startValue - picDrawY
    '                        startValue = picDrawY
    '                        If haveColorPre = True Then
    '
    '                            drawLength = drawLength - 1
    '                            If shutterIsOpen = False Then
    '                                shutterOpen
    '                            End If
    '                            If drawLength = 1 Then
    '                                drawLength = 0
    '                                flagExtra = True
    '                            End If
    '                            If drawLength > 0 Then
    '                                delayAccurate (1 / Val(vel) * 10000)
    '                                ypic = Str(1 * drawLength)
    '                                Xpic = Str(0)
    '                                lpic = Xpic + blank + ypic + blank + run + enter
    '                                MSComm1.Output = lpic
    '                                CorYV.Text = CorYV.Text + drawLength
    '                                Text1.Text = "y" & drawLength
    '                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
    '                                delayAccurate (1 / Val(vel) * 10000)
    '                            ElseIf drawLength = 0 Then
    '                                delayAccurate (1 / Val(vel) * 10000 + 200)
    '                            End If
    '
    '                            If shutterIsOpen = True Then
    '                                shutterClose
    '                            End If
    '
    '                        ElseIf haveColorPre = False Then
    '
    '
    '                            drawLength = drawLength + 1
    '                            If shutterIsOpen = True Then
    '                                shutterClose
    '                            End If
    '                            If flagExtra = True Then
    '                                drawLength = drawLength + 1
    '                                flagExtra = False
    '                            End If
    '                            ypic = Str(1 * drawLength)
    '                            Xpic = Str(0)
    '                            lpic = Xpic + blank + ypic + blank + run + enter
    '                            MSComm1.Output = lpic
    '                            CorYV.Text = CorYV.Text + drawLength
    '                            Text1.Text = "y" & drawLength
    '                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
    '                        End If
    '
    '                        If haveColorNow = True Then
    '
    '                            If shutterIsOpen = False Then
    '                                shutterOpen
    '                            End If
    '
    '                            delayAccurate (1 / Val(vel) * 10000 + 200)
    '
    '                        ElseIf haveColorNow = False Then
    '
    '                            If shutterIsOpen = True Then
    '                                shutterClose
    '                            End If
    '
    '                            drawLength = 1
    '                            If flagExtra = True Then
    '                                drawLength = drawLength + 1
    '                                flagExtra = False
    '                            End If
    '                            ypic = Str(1 * drawLength)
    '                            Xpic = Str(0)
    '                            lpic = Xpic + blank + ypic + blank + run + enter
    '                            MSComm1.Output = lpic
    '                            CorYV.Text = CorYV.Text + drawLength
    '                            Text1.Text = "y" & drawLength
    '                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
    '
    '                        End If
                        
                        End If
                        
    
                        
    
                        
                        If shutterIsOpen = True Then
                            shutterClose
                        End If
                        ypic = Str(0)
                        Xpic = Str(StepSizeX)
                        
                        lpic = Xpic + blank + ypic + blank + run + enter
                        MSComm1.Output = lpic
                        CorXV.Text = CorXV.Text + 1
                        Text14.Text = Text14.Text + 1
                        delayAccurate (2 * StepSizeX / Val(vel) * 10000 + 200)
                        
                        If picDrawX < picWidth Then
                        
                            If newPixelPannel(picDrawX + 1, 1) < picRegionMax Then
                                If newPixelPannel(picDrawX + 1, 1) > picRegionMin Then
                                    haveColorNow = True
                                End If
    '                        ElseIf newpixelpannel(picDrawX + 1, 1) > picRegionMin Then
                            Else
                                haveColorNow = False
                            End If
                            
                        End If
                        
                    End If
                    
                    haveColorPre = haveColorNow
          
                Next
            End If
            
        ElseIf flagDrawPicPause1 = True Then
            If flagDrawpicAbort1 = True Then
                Text14.Text = 1
                Text1.Text = ""
                drawPicStatus.Cls
                drawPicStatus.FontSize = 10
                drawPicStatus.Print "Aborted"
            End If
            
            DrawPicStartValue = picDrawX + 1
            t = sec.Text + 60 * min.Text + 3600 * hour.Text
            Timer1.Enabled = False
            Exit For
        
        End If

        If picDrawX / progressDivide > progressNum Then
            progressNum = progressNum + 1
            DrawPicProgress.Print "l";
        End If

    Next

End Sub



'initialize
'initialize
'initialize
'initialize
'initialize

Public Sub Position_Initialize()
    
        picLogo.Left = 120
        picLogo.Top = 1320
        picLogo.Height = 6135
        picLogo.Width = 7035
        picLogo.Visible = True
        
        stage_frame.Left = 120
        stage_frame.Top = 1800
        stage_frame.Height = 6495
        stage_frame.Width = 7005
        stage_frame.Visible = False
        
        rastor_frame.Height = 2655
        rastor_frame.Left = 1980
        rastor_frame.Top = 3240
        rastor_frame.Width = 3555
        rastor_frame.Visible = False
        
        arrow_frame.Left = 1560
        arrow_frame.Top = 3120
        arrow_frame.Height = 3255
        arrow_frame.Width = 4455
        arrow_frame.Visible = False
        
        Print_Frame.Height = 2895
        Print_Frame.Left = 1440
        Print_Frame.Top = 3360
        Print_Frame.Width = 4455
        
        shutterControl.Height = 2415
        shutterControl.Left = 900
        shutterControl.Top = 3500
        shutterControl.Width = 2715
        
        laser_power_frame.Height = 2415
        laser_power_frame.Left = 3720
        laser_power_frame.Top = 3500
        laser_power_frame.Width = 2715
        
        drawPic_frame.Height = 3615
        drawPic_frame.Left = 1980
        drawPic_frame.Top = 2500
        drawPic_frame.Width = 3795
        
        Advance_Option.Height = 2415
        Advance_Option.Left = 2760
        Advance_Option.Top = 3600
        Advance_Option.Width = 2175
        
        Port_Warning.Height = 615
        Port_Warning.Left = 1200
        Port_Warning.Top = 1800
        Port_Warning.Width = 5895
        
        Command3.Visible = False
        shutterControl.Visible = False
        drawPic_frame.Visible = False
        laser_power_frame.Visible = False
        Warning_frame.Visible = False
        MultiRastor.Visible = False
        test_frame.Visible = False
        MoveMultiRastor.Visible = False
        'Command_Multi_Rastor.Visible = False
        'fordebug.Visible = False
        'drawPic_frame.Visible = False
        Print_Frame.Visible = False
        'LaserPrint_frame.Visible = False
        
        
        
End Sub


Public Sub parameter_initialize()

    xmove = 0
    ymove = 0
    checkX = 1
    checkY = 1
    zero = Str(0)
    temp2 = Str(1)
    temp = Str(1)
    StageMovementSwitch.Caption = "Stage"
    ArrowControlSwitch.Caption = "Stage"
    flagStage = 1
    flagDisStage = 1
    positionX = 0
    positionY = 0
    flagDelay = 1
    acStep = 1
    AccuracyStep.Text = acStep
    tempVS = ""
    tempVR = ""
    tempVA = 100
    flagFirst = 1
    flagArrowKey = 0
    flagToyBox = 0
    WorldX = 0
    WorldY = 0
    CorXV.Text = 0
    CorYV.Text = 0
    printType1 = False
    printType2 = False
    FontChoice.AddItem "Times New Roman"
    FontChoice.AddItem "Sogoe Print"
    flagMultiDirection = 1
    flagMultiOrder = 1
    flagMultiRastor = False
    laserMotorFreq = 200
    allowPowerChange = True
    powerStepDelay = 3333
    drawing_mode = 1
    DrawPicExtraBoundry = 50
    t = 0
    
    'Text2.Text = 10 Mod 2
    
    StageControl.KeyPreview = True
'    ToyF.Height = 375
'    ToyF.Width = 1095
    'arrow_frame.Left = 1320
    'arrow_frame.Top = 2600
    'flagCircleFirst = 1
    'flagInputRadius = 0
    'flagStartingPoint = 0
    laserStep = 8
    laserPosition = 0
    shutterIsOpen = False
    shutterControlLoop = 1
    ShutterControlOnTime = 1
    ShutterControlOffTime = 1
    flagPrintMode = 0
    picDrawCorrect = 130
    flagPrintEnd = True
    flagDrawPicPause1 = False
    
    inputData
    
End Sub



Private Sub input_FontPixel()

    Dim picHandleX As Long
    Dim picHandleY As Long
    Dim r As Byte
    Dim g As Byte
    Dim b As Byte
    Dim ri As Integer
    Dim gi As Integer
    Dim bi As Integer
    Dim alpha As Byte
    Dim currentPixel As Long
    

    currentPixel = 0
    
    

    
    Get #1, , PicInfo

    fontWidth = Abs(PicInfo.bmiHeader.biWidth)
    fontHeight = Abs(PicInfo.bmiHeader.biHeight)

    ReDim pixelPannel(1 To fontWidth, 1 To fontHeight)


    'filelen = PicInfo.bmiHeader.biSizeImage
    

    For picHandleY = fontHeight To 1 Step -1

        For picHandleX = 1 To fontWidth
            currentPixel = currentPixel + 1
            Get #1, , b
            Get #1, , g
            Get #1, , r
            Get #1, , alpha
            ri = r
            gi = g
            bi = b
            pixelPannel(picHandleX, picHandleY) = (ri + gi + bi) / 3
'            newPixelPannel(2 * picHandleX - 1, 2 * picHandleY - 1) = (ri + gi + bi) / 3
'            newPixelPannel(2 * picHandleX - 1, 2 * picHandleY) = (ri + gi + bi) / 3
'            newPixelPannel(2 * picHandleX, 2 * picHandleY - 1) = (ri + gi + bi) / 3
'            newPixelPannel(2 * picHandleX, 2 * picHandleY) = (ri + gi + bi) / 3
        Next

    Next
    
    ReDim FontPixel(1 To fontWidth, 1 To fontHeight)
    For picHandleX = 1 To fontWidth
        For picHandleY = 1 To fontHeight
            FontPixel(picHandleX, picHandleY) = pixelPannel(picHandleX, picHandleY)
        Next

    Next
    
    
'    drawPicStatus.Cls
'
'    drawPicStatus.Print "   Completed"

    Close #1

End Sub

Private Sub input_FontLocation()

    ReDim FontLocation(1 To 5, 1 To 13)
    
    Dim thisrow, thiscol As Integer
    Dim thisi, thisj As Integer
    Dim thisstart, thisend As Integer
    Dim flagThisStart As Boolean
    Dim flagHaveFont As Boolean
    Dim flagFindX As Boolean
    flagFindX = False
    Dim FontDevideY(1 To 10) As Integer

    flagThisStart = False
    
    thisi = 1
    For thisj = 1 To fontHeight
    
        If FontPixel(1, thisj) < 200 Then
            For thiscol = 1 To fontWidth
                FontPixel(thiscol, thisj) = 255
            Next
            FontDevideY(thisi) = thisj
            thisi = thisi + 1
        End If
    
    Next
        
    For thiscol = 1 To 13
        FontLocation(1, thiscol).StartY = FontDevideY(1)
        FontLocation(1, thiscol).EndY = FontDevideY(2)
        FontLocation(2, thiscol).StartY = FontDevideY(3)
        FontLocation(2, thiscol).EndY = FontDevideY(4)
        FontLocation(3, thiscol).StartY = FontDevideY(5)
        FontLocation(3, thiscol).EndY = FontDevideY(6)
        FontLocation(4, thiscol).StartY = FontDevideY(7)
        FontLocation(4, thiscol).EndY = FontDevideY(8)
        FontLocation(5, thiscol).StartY = FontDevideY(9)
        FontLocation(5, thiscol).EndY = FontDevideY(10)
    Next
    
    thiscol = 1
    
    For thisrow = 1 To 5
        thiscol = 1
        For thisi = 1 To fontWidth
            flagHaveFont = False
            
            For thisj = FontLocation(thisrow, 1).StartY To FontLocation(thisrow, 1).EndY
            
                If FontPixel(thisi, thisj) < 200 Then
                    flagHaveFont = True
                End If
                                
            Next
            
            If flagHaveFont = True Then
                If flagThisStart = False Then
                    flagThisStart = True
                    FontLocation(thisrow, thiscol).StartX = thisi - 1
                End If
            ElseIf flagHaveFont = False Then
                If flagThisStart = True Then
                    flagThisStart = False
                    FontLocation(thisrow, thiscol).EndX = thisi + 1
                    If (FontLocation(thisrow, thiscol).StartX - FontLocation(thisrow, thiscol).EndX) Mod 2 = 0 Then
                        FontLocation(thisrow, thiscol).EndX = FontLocation(thisrow, thiscol).EndX + 1
                    End If
                    thiscol = thiscol + 1
                End If
            End If
        Next
    Next
End Sub


Public Sub drawFont(thisX As Integer, thisY As Integer)

    Dim picDrawX As Integer
    Dim picDrawY As Integer
    Dim startValue As Integer
    Dim endValue As Integer
    Dim sameRegion As Boolean

    Dim haveColorPre As Boolean
    Dim haveColorNow As Boolean
    Dim iniP As Boolean
    Dim Xpic, ypic As String
    Dim flagExtra As Boolean
    Dim countFontCorrect As Integer
    Dim startThisX, endThisX, startThisY, endThisY As Integer
    'Dim flagCorrect As bollean
    startThisX = FontLocation(thisX, thisY).StartX
    startThisY = FontLocation(thisX, thisY).StartY
    endThisX = FontLocation(thisX, thisY).EndX
    endThisY = FontLocation(thisX, thisY).EndY

    
    countFontCorrect = 0
    'flagCorrect = False

    flagExtra = False


        sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent


'        lpic = Xpic + blank + Ypic + blank + run + enter


    
    If FontPixel(startThisX, startThisY) < picRegionMax Then
        If FontPixel(endThisX, endThisY) > picRegionMin Then
            haveColorPre = True
        End If
'    ElseIf FontPixel(1, 1) > picRegionWhite Then
    Else
        haveColorPre = False
    End If
    
    If shutterIsOpen = True Then
        shutterClose
    End If
    
    
'    ypic = Str(-10)
'    xpic = Str(0)
'    lpic = xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(ypic) / Val(vel)) * 10000 + 1000)
'
'    ypic = Str(0)
'    xpic = Str(-10)
'    lpic = xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(xpic) / Val(vel)) * 10000 + 1000)
'
'    ypic = Str(10)
'    xpic = Str(0)
'    lpic = xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(ypic) / Val(vel)) * 10000 + 1000)
'
'    ypic = Str(0)
'    xpic = Str(10)
'    lpic = xpic + blank + ypic + blank + run + enter
'    MSComm1.Output = lpic
'    delayAccurate (Abs(Val(xpic) / Val(vel)) * 10000 + 1000)
    
    picHeight = picHeight
    
    For picDrawX = startThisX To endThisX
        If (picDrawX - startThisX + 1) Mod 2 = 1 Then
        ypic = Str(2 * -1)
        Xpic = Str(0)
        lpic = Xpic + blank + ypic + blank + run + enter
        MSComm1.Output = lpic
        delayAccurate (Abs(Val(Xpic) / Val(vel)) * 10000 + 1000)
            For picDrawY = startThisY To endThisY
            
                If FontPixel(picDrawX, picDrawY) < picRegionMax Then
                    If FontPixel(picDrawX, picDrawY) > picRegionMin Then
                        haveColorNow = True
                    End If
'                ElseIf FontPixel(picDrawX, picDrawY) > picRegionWhite Then
                Else
                    haveColorNow = False
                End If
                
                If haveColorNow = haveColorPre Then
                    sameRegion = True
                Else
                    sameRegion = False
                End If
                

                If picDrawY = startThisY Then
                    startValue = startThisY
                End If
                
                If picDrawY < endThisY Then
                
                    If sameRegion = False Then
                        drawLength = picDrawY - startValue
                        
                        If haveColorPre = True Then
                        
                            drawLength = drawLength - 1
'                            If drawLength = 1 Then
'                                drawLength = 0
'                                flagExtra = True
'                            End If
                            If shutterIsOpen = False Then
                                shutterOpen
                            End If

                            If drawLength > 0 Then
                                delayAccurate (1 / Val(vel) * 10000)
                                ypic = Str(-1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text - drawLength
                                Text1.Text = "y-" & drawLength
                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                delayAccurate (1 / Val(vel) * 10000)
                                
                                countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If
                            ElseIf drawLength = 0 Then
                                delayAccurate (1 / Val(vel) * 10000 + 200)
                            End If
                            
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            
                        ElseIf haveColorPre = False Then
                            
                            If startValue = startThisY Then
                                drawLength = drawLength
                            Else
                                drawLength = drawLength + 1
                            End If
'                            If flagExtra = True Then
'                                drawLength = drawLength + 1
'                                flagExtra = False
'                            End If
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            ypic = Str(-1 * drawLength)
                            Xpic = Str(0)
                            lpic = Xpic + blank + ypic + blank + run + enter
                            MSComm1.Output = lpic
                            'countnum
                            CorYV.Text = CorYV.Text - drawLength
                            Text1.Text = "y-" & drawLength
                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
                            
                            countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If

                        End If
                            
                        startValue = picDrawY
                            
                    End If
                
                
                ElseIf picDrawY = endThisY Then
                    If sameRegion = True Then
                        If haveColorNow = True Then
                        
                            drawLength = endThisY - startValue
                            If shutterIsOpen = False Then
                                shutterOpen
                            End If
'                            If drawLength = 1 Then
'                                drawLength = 0
'                                flagExtra = True
'                            End If
                            If drawLength > 0 Then
                               delayAccurate (1 / Val(vel) * 10000)
                               ypic = Str(-1 * drawLength)
                               Xpic = Str(0)
                               lpic = Xpic + blank + ypic + blank + run + enter
                               MSComm1.Output = lpic
                               'countnum
                               CorYV.Text = CorYV.Text - drawLength
                               Text1.Text = "y-" & drawLength
                               delayAccurate (drawLength / Val(vel) * 10000 + 200)
                               delayAccurate (1 / Val(vel) * 10000)
                               
                               countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If

                            ElseIf drawLength = 0 Then
                                delayAccurate (1 / Val(vel) * 10000 + 200)
                            End If
                            
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                        
                        ElseIf haveColorNow = False Then
                        
                            drawLength = endThisY + 1 - startValue
'                            If flagExtra = True Then
'                                drawLength = drawLength + 1
'                                flagExtra = False
'                            End If
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            ypic = Str(-1 * drawLength)
                            Xpic = Str(0)
                            lpic = Xpic + blank + ypic + blank + run + enter
                            MSComm1.Output = lpic
                            'countnum
                            'CorYV.Text = CorYV.Text - drawLength
                            Text1.Text = "y-" & drawLength
                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
                            
                            countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If

                        
                        End If

                    
                    End If
                    


        
                
                    
                    If shutterIsOpen = True Then
                        shutterClose
                    End If
                    ypic = Str(0)
                    Xpic = Str(1)
                    
                    lpic = Xpic + blank + ypic + blank + run + enter
                    MSComm1.Output = lpic
                    CorXV.Text = CorXV.Text + 1
                    Text1.Text = "x+1"
                    delayAccurate (1 / Val(vel) * 10000 + 200)
                    
                    If picDrawX < endThisX Then
                    
                        If FontPixel(picDrawX + 1, endThisY) < picRegionMax Then
                            If FontPixel(picDrawX + 1, endThisY) > picRegionMin Then
                                haveColorNow = True
                            End If
                        
'                        ElseIf FontPixel(picDrawX + 1, picHeight) > picRegionMin Then
                        Else
                            haveColorNow = False
                        End If
                        
                    End If
                    
                End If
                
                haveColorPre = haveColorNow
      
            Next
            
        ElseIf (picDrawX - startThisX + 1) Mod 2 = 0 Then
        ypic = Str(2)
        Xpic = Str(0)
        lpic = Xpic + blank + ypic + blank + run + enter
        MSComm1.Output = lpic
        delayAccurate (Abs(Val(Xpic) / Val(vel)) * 10000 + 1000)
            For picDrawY = endThisY To startThisY Step -1
            
                If FontPixel(picDrawX, picDrawY) < picRegionMax Then
                    If FontPixel(picDrawX, picDrawY) > picRegionMin Then
                        haveColorNow = True
                    End If
'                ElseIf FontPixel(picDrawX, picDrawY) > picRegionMin Then
                Else
                    haveColorNow = False
                End If
                
                If haveColorNow = haveColorPre Then
                    sameRegion = True
                Else
                    sameRegion = False
                End If
                

                If picDrawY = endThisY Then
                    startValue = endThisY
                End If
                
                If picDrawY > startThisY Then
                
                    If sameRegion = False Then
                        drawLength = startValue - picDrawY
                        
                        If haveColorPre = True Then
                        
                            drawLength = drawLength - 1
                            If shutterIsOpen = False Then
                                shutterOpen
                            End If
'                            If drawLength = 1 Then
'                                drawLength = 0
'                                flagExtra = True
'                            End If
                            If drawLength > 0 Then
                                delayAccurate (1 / Val(vel) * 10000)
                                ypic = Str(1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text + drawLength
                                Text1.Text = "y" & drawLength
                                delayAccurate (drawLength / Val(vel) * 10000 + 200)
                                delayAccurate (1 / Val(vel) * 10000)
                                
                                countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If

                            ElseIf drawLength = 0 Then
                                delayAccurate (1 / Val(vel) * 10000 + 200)
                            End If
                            
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            
                        ElseIf haveColorPre = False Then
                                
                            If startValue = endThisY Then
                                drawLength = drawLength
                            Else
                                drawLength = drawLength + 1
                            End If
'                            If flagExtra = True Then
'                                drawLength = drawLength + 1
'                                flagExtra = False
'                            End If
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                            ypic = Str(1 * drawLength)
                            Xpic = Str(0)
                            lpic = Xpic + blank + ypic + blank + run + enter
                            MSComm1.Output = lpic
                            'countnum
                            CorYV.Text = CorYV.Text + drawLength
                            Text1.Text = "y" & drawLength
                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
                            
                            countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If

                        End If
                        startValue = picDrawY
                    End If
                
                
                ElseIf picDrawY = startThisY Then
                    If sameRegion = True Then
                        If haveColorNow = True Then
                        
                            drawLength = startValue - startThisY
                            If shutterIsOpen = False Then
                                shutterOpen
                            End If
'                            If drawLength = 1 Then
'                                drawLength = 0
'                                flagExtra = True
'                            End If
                            If drawLength > 0 Then
                               delayAccurate (1 / Val(vel) * 10000)
                               ypic = Str(1 * drawLength)
                               Xpic = Str(0)
                               lpic = Xpic + blank + ypic + blank + run + enter
                               MSComm1.Output = lpic
                               'countnum
                               CorYV.Text = CorYV.Text + drawLength
                               Text1.Text = "y" & drawLength
                               delayAccurate (drawLength / Val(vel) * 10000 + 200)
                               delayAccurate (1 / Val(vel) * 10000)
                               
                               countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If

                            ElseIf drawLength = 0 Then
                                delayAccurate (1 / Val(vel) * 10000 + 200)
                            End If
                            
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
                        
                        ElseIf haveColorNow = False Then

                            drawLength = startValue - startThisY + 1
                            If shutterIsOpen = True Then
                                shutterClose
                            End If
'                            If flagExtra = True Then
'                                drawLength = drawLength + 1
'                                flagExtra = False
'                            End If
                            ypic = Str(1 * drawLength)
                            Xpic = Str(0)
                            lpic = Xpic + blank + ypic + blank + run + enter
                            MSComm1.Output = lpic
                            'countnum
                            CorYV.Text = CorYV.Text + drawLength
                            Text1.Text = "y" & drawLength
                            delayAccurate (drawLength / Val(vel) * 10000 + 200)
                            
                            countFontCorrect = countFontCorrect + 1
                                If countFontCorrect > fontDrawCorrect Then
                                    ypic = Str(-1)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    MSComm1.Output = lpic
                                    delayAccurate (1 / Val(vel) * 10000)
                                    countFontCorrect = 1
                                End If


                        End If

                    
                    End If
                    

                    

                    
                    If shutterIsOpen = True Then
                        shutterClose
                    End If
                    ypic = Str(0)
                    Xpic = Str(1)
                    
                    lpic = Xpic + blank + ypic + blank + run + enter
                    MSComm1.Output = lpic
                    CorXV.Text = CorXV.Text + 1
                    Text1.Text = "x+1"
                    delayAccurate (1 / Val(vel) * 10000 + 200)
                    
                    If picDrawX < picWidth Then
                    
                        If FontPixel(picDrawX + 1, 1) < picRegionMax Then
                            If FontPixel(picDrawX + 1, 1) > picRegionMin Then
                                haveColorNow = True
                            End If
'                        ElseIf FontPixel(picDrawX + 1, 1) > picRegionMin Then
                        Else
                            haveColorNow = False
                        End If
                        
                    End If
                    
                End If
                
                haveColorPre = haveColorNow
      
            Next
        End If
    Next

End Sub


Private Sub Form_Initialize()
   
    MSComm1.PortOpen = True
    
    enter = Chr(13)
    blank = Chr(32)
    run = Chr(114)
    For i = 1 To 6
    Steps.AddItem i
    Next i
    
    parameter_initialize
    
    Position_Initialize
    
    StageControl.KeyPreview = True
    

          
End Sub


Private Sub Form_LostFocus()

    MSComm1.PortOpen = False
    
End Sub


Private Sub Freq_Change()

    StepFreq = Freq.Text

End Sub






Private Sub Laser_Close_Click()

    shutterClose
    Laser_Close.Height = 375
    Laser_Close.Top = 8400
    Laser_Close.Left = 6120
    Laser_Close.Width = 615
    'Laser_Close.BackColor = &H8080FF
    
    Laser_Open.Height = 375
    Laser_Open.Top = 8400
    Laser_Open.Left = 1440
    Laser_Open.Width = 4695
    'Laser_Open.BackColor = &H80FF80

End Sub

Private Sub Laser_Open_Click()

    Laser_Open.Height = 375
    Laser_Open.Top = 8400
    Laser_Open.Left = 1440
    Laser_Open.Width = 615
    'Laser_Open.BackColor = &H8080FF
    
    Laser_Close.Height = 375
    Laser_Close.Top = 8400
    Laser_Close.Left = 2055
    Laser_Close.Width = 4695
    'Laser_Close.BackColor = &H80FF80
    
'    If shutterIsOpen = False Then
'        delayAccurate (600000)
'        Laser_Close_Click
'    End If
    
    shutterOpen

    

End Sub


Public Sub shutterClose()

    StepFreq = 1000
    out Val("&H378"), Val(1)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(0)
    delayAccurate (1 / StepFreq * 10000)
        
    shutterIsOpen = False

End Sub


Public Sub shutterOpen()

    StepFreq = 1000
    out Val("&H378"), Val(11)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(10)
    delayAccurate (1 / StepFreq * 10000)
    
    shutterIsOpen = True

End Sub



'mode choose
'mode choose
'mode choose
'mode choose
'mode choose


Private Sub stage_Click()
    
    If flagMode = 2 Then
        tempVR = velocity.Text
    ElseIf flagMode = 3 Then
        tempVA = velocity.Text
    End If
    
    flagMode = 1
    If flagMode = 2 Then
        temp = XLoop.Text
    End If
    
    velocity.Text = tempVS

    stagepic.Cls
    
    stagepic.Print "   On"
    
    rastorpic.Cls
    
    rastorpic.Print "   Off"
    
    arrowpic.Cls
    
    arrowpic.Print "   Off"
    
    Steps.Visible = True
    Go.Visible = True
    XLoop.Visible = True
    velocity.Visible = True
    LoopNum.Visible = True
    Label13.Visible = True
    Label16.Visible = True
    Label17.Visible = True
    MoveStart.Visible = True
    'ToyF.Visible = False
    
    'StageControl.KeyPreview = False
    
    
    stage_frame.Visible = True
    rastor_frame.Visible = False
    arrow_frame.Visible = False
    picLogo.Visible = False
    
    XLoop.Text = temp2
     
    If XLoop.Text = "" Then
        XLoop.Text = 1
    End If

    
    If Val(Steps.Text) = 1 Then
        stage_frame1.Visible = True
        stage_frame2.Visible = False
        stage_frame3.Visible = False
        stage_frame4.Visible = False
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 2 Then
        
        
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = False
        stage_frame4.Visible = False
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
        
        
    ElseIf Val(Steps.Text) = 3 Then
        
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = False
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 4 Then
    
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = True
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 5 Then
    
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = True
        stage_frame5.Visible = True
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 6 Then
        
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = True
        stage_frame5.Visible = True
        stage_frame6.Visible = True
        
    End If
    

    Command3.Visible = False
    shutterControl.Visible = False
    drawPic_frame.Visible = False
    laser_power_frame.Visible = False
    Warning_frame.Visible = False
    MultiRastor.Visible = False
    test_frame.Visible = False
    'Command_Multi_Rastor.Visible = False
    'fordebug.Visible = False
    'drawPic_frame.Visible = False
    Print_Frame.Visible = False
    'LaserPrint_frame.Visible = False


End Sub


Private Sub rastor_Click()

    If flagMode = 1 Then
        tempVS = velocity.Text
    ElseIf flagMode = 3 Then
        tempVA = velocity.Text
    End If
    
    flagMode = 2
    If flagMode = 1 Then
        temp2 = XLoop.Text
    End If
    
    
    velocity.Text = tempVR
    
    stagepic.Cls
    
    stagepic.Print "   Off"
    
    rastorpic.Cls
    
    rastorpic.Print "   On"
    
    arrowpic.Cls
    
    arrowpic.Print "   Off"
    
    XLoop.Text = temp
    
    'StageControl.KeyPreview = False
    
    arrow_frame.Visible = False
    stage_frame.Visible = False
    rastor_frame.Visible = True
    picLogo.Visible = False
    
    MoveStart.Visible = True
    'ToyF.Visible = False
    
    'Steps.Text = "# of steps"
    Steps.Visible = False
    Go.Visible = False
    XLoop.Visible = True
    velocity.Visible = True
    LoopNum.Visible = True
    Label13.Visible = True
    Label16.Visible = True
    Label17.Visible = True
    

    Command3.Visible = False
    shutterControl.Visible = False
    drawPic_frame.Visible = False
    laser_power_frame.Visible = False
    Warning_frame.Visible = False
    MultiRastor.Visible = False
    test_frame.Visible = False
    'Command_Multi_Rastor.Visible = False
    'fordebug.Visible = False
    'drawPic_frame.Visible = False
    Print_Frame.Visible = False
    'LaserPrint_frame.Visible = False
    

End Sub

Private Sub arrow_Click()

    If flagMode = 2 Then
        tempVR = velocity.Text
        temp = XLoop.Text
    ElseIf flagMode = 1 Then
        tempVS = velocity.Text
    End If
    
    flagMode = 3
    flagFirst = 1
    
    If flagDisStage = 1 Then
        positionX = -1 * positionX
        positionY = -1 * positionY
        WorldX = positionX
        WorldY = positionY
    ElseIf flagDisStage = 0 Then
        positionX = positionX
        positionY = positionY
        WorldX = -1 * WorldX
        WorldY = -1 * WorldY
    End If
    
    
    
    velocity.Text = tempVA
    
    stagepic.Cls
    
    stagepic.Print "   Off"
    
    rastorpic.Cls
    
    rastorpic.Print "   Off"
    
    arrowpic.Cls
    
    arrowpic.Print "   On"
    
    arrow_frame.Visible = True
    rastor_frame.Visible = False
    stage_frame.Visible = False
    picLogo.Visible = False

    MoveStart.Visible = False
    'ToyF.Visible = False
    
    StageControl.KeyPreview = True
    
    arrowXpic.Cls
    
    arrowXpic.ForeColor = &HFF00&
    
    arrowXpic.Print positionX
    
    CorXV = positionX
    
    
    arrowYpic.Cls

    arrowYpic.ForeColor = &HFF00&

    arrowYpic.Print positionY
    
    CorYV = positionY
    
    Steps.Visible = False
    Go.Visible = False
    XLoop.Visible = False
    LoopNum.Visible = False
    velocity.Visible = True
    Label13.Visible = True
    Label16.Visible = True
    Label17.Visible = True
       
       
       
    Command3.Visible = False
    shutterControl.Visible = False
    drawPic_frame.Visible = False
    laser_power_frame.Visible = False
    Warning_frame.Visible = False
    MultiRastor.Visible = False
    test_frame.Visible = False
    'Command_Multi_Rastor.Visible = False
    'fordebug.Visible = False
    'drawPic_frame.Visible = False
    Print_Frame.Visible = False
    'LaserPrint_frame.Visible = False

End Sub

Private Sub Command_Shutter_Control_Click()

    flagMode = 4

    StageControl.KeyPreview = True
    
    arrow_frame.Visible = False
    stage_frame.Visible = False
    rastor_frame.Visible = False
    Command3.Visible = False
    laser_power_frame.Visible = False
    Warning_frame.Visible = False
    MultiRastor.Visible = False
    test_frame.Visible = False
    'Command_Multi_Rastor.Visible = False
    'fordebug.Visible = False
    'drawPic_frame.Visible = False
    'LaserPrint_frame.Visible = False
    picLogo.Visible = False
    Print_Frame.Visible = False
    
    shutterControl.Visible = True
    drawPic_frame.Visible = False
    laser_power_frame.Visible = True

End Sub


Private Sub Command_Print_Click()

    flagMode = 5
    fontDrawCorrect = 130
    countFontCorrect = 0
    
    

    
    
    StageControl.KeyPreview = True
    
    Label13.Visible = True
    Label16.Visible = True
    Label17.Visible = True
    velocity.Visible = True
    velocity.Text = 100
    arrow_frame.Visible = False
    stage_frame.Visible = False
    rastor_frame.Visible = False
    Command3.Visible = False
    shutterControl.Visible = False
    drawPic_frame.Visible = False
    laser_power_frame.Visible = False
    Warning_frame.Visible = False
    MultiRastor.Visible = False
    test_frame.Visible = False
    'Command_Multi_Rastor.Visible = False
    'fordebug.Visible = False
    'drawPic_frame.Visible = False
    'LaserPrint_frame.Visible = False
    picLogo.Visible = False
    
    Print_Frame.Visible = True

End Sub

Private Sub Command_Print_Pic_Click()

    flagMode = 6

    
    
    StageControl.KeyPreview = True
    
    Label13.Visible = True
    Label16.Visible = True
    Label17.Visible = True
    velocity.Visible = True
    velocity.Text = 100
    arrow_frame.Visible = False
    stage_frame.Visible = False
    rastor_frame.Visible = False
    Command3.Visible = False
    shutterControl.Visible = False
    laser_power_frame.Visible = False
    Warning_frame.Visible = False
    MultiRastor.Visible = False
    test_frame.Visible = False
    'Command_Multi_Rastor.Visible = False
    'fordebug.Visible = False
    'drawPic_frame.Visible = False
    'LaserPrint_frame.Visible = False
    picLogo.Visible = False
    Print_Frame.Visible = False
    
    drawPic_frame.Visible = True
    
    If drawing_mode = 1 Then
    
        Pic_mode1.Value = True
    
    ElseIf drawing_mode = 2 Then
        
        Pic_mode2.Value = True
        
    End If
    

End Sub





Public Sub FontChoice_click()

    If FontChoice.Text = "Times New Roman" Then
        Open (App.Path & "\font\TimesNewRoman.font") For Binary As #1
        input_FontPixel
        input_FontLocation
    ElseIf FontChoice.Text = "Sogoe Print" Then
        Open (App.Path & "\font\SogoePrint.font") For Binary As #1
        input_FontPixel
        input_FontLocation
    End If

End Sub

'side function
'side function
'side function
'side function
'side function



Private Sub reset_Click()

    ypic.Cls
    If flagMode = 1 Then
    
        xinput1.Text = ""
        yinput1.Text = ""
        xinput2.Text = ""
        yinput2.Text = ""
        xinput3.Text = ""
        yinput3.Text = ""
        xinput4.Text = ""
        yinput4.Text = ""
        xinput5.Text = ""
        yinput5.Text = ""
        xinput6.Text = ""
        yinput6.Text = ""
        XLoop.Text = Str("1")
        Tinput1.Text = Str("0")
        velocity.Text = ""
        
    ElseIf flagMode = 2 Then
        
        xinputR.Text = ""
        yinputR.Text = ""
        step1.Text = Str("1")
        step2.Text = Str("1")
        velocity.Text = ""
        rustY.Value = 0
        rustX.Value = 0
        XLoop.Text = Str("1")
        
    ElseIf flagMode = 3 Then
        
        AccuracyStep.Text = 1
        velocity.Text = 100
        positionX = 0
        positionY = 0
        arrowXpic.Cls
    
        arrowXpic.ForeColor = &HFF00&
        
        arrowXpic.Print positionX
        
        CorXV = positionX
        
        arrowYpic.Cls
    
        arrowYpic.ForeColor = &HFF00&
    
        arrowYpic.Print positionY
        
        CorYV = positionY
    
    End If
        
    StageMovementSwitch.Caption = "Stage"
    flagStage = 1
    
End Sub





Private Sub Abort_Click()
    
    
    
    If flagMode = 6 Then
        flagDrawPicPause1 = True
        flagDrawpicAbort1 = True
        DrawPicPause.Caption = "Pause"
        sec.Text = 0
        min.Text = 0
        hour.Text = 0
        Text14.Text = 1
        Text1.Text = ""
        drawPicStatus.Cls
        drawPicStatus.FontSize = 10
        drawPicStatus.Print "Executing"
        DrawPicProgress.Cls

    Else
    
        ypic.Cls
    
        ypic.Print "Executing"
        
        flagStop = 1
        t = 1
        SoundName$ = vbNullString
            wFlags% = SND_ASYNC Or SND_NODEFAULT
            X% = sndPlaySound(SoundName$, wFlags%)
    End If

End Sub












Private Sub StopMusic_Click()

    SoundName$ = vbNullString
    wFlags% = SND_ASYNC Or SND_NODEFAULT
    X% = sndPlaySound(SoundName$, wFlags%)

End Sub


Private Sub Exit_Click()
    
    
    ' DrawPicMin  DrawPicMax
    SaveData
    SoundName$ = vbNullString
    wFlags% = SND_ASYNC Or SND_NODEFAULT
    X% = sndPlaySound(SoundName$, wFlags%)
    MSComm1.PortOpen = False
    Unload Me
    

End Sub



Private Sub MoveStart_Click()
   
   
    If shutterIsOpen = False Then
        shutterOpen
    End If
    checkZeroFix
    checkZeroWarning
    If flagWarning = 0 Then
        sent = "-5000 -5000 5000 5000 setlimit" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        
        sent = "1 1 setunit" + enter ' x axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 2 setunit" + enter ' y axis
        Debug.Print sent
        MSComm1.Output = sent
        
        sent = "1 0 setunit" + enter ' velocity
        Debug.Print sent
        MSComm1.Output = sent
    
        sent = vel + "setvel" + enter
        Debug.Print sent
        MSComm1.Output = sent
        
        
        T1 = 0
        T2 = 0
        T3 = 0
        T4 = 0
        T5 = 0
        T6 = 0
        
      
        If flagDisStage = 0 Then
        
            positionX = positionX
            positionY = positionY
        ElseIf flagDisStage = 1 Then
            positionX = -1 * positionX
            positionY = -1 * positionY
        End If
        
        
        
           
        If flagMode = 2 Then
            
            
            If Abs(Val(XR)) > Abs(Val(YR)) Then
                TR = (Abs(Val(XR) ^ 2) + Abs(Val(YR) ^ 2)) ^ (1 / 2) / Val(vel)
                VR = Str(Abs(Val(XR)) / TR)
            Else
                TR = (Abs(Val(XR) ^ 2) + Abs(Val(YR) ^ 2)) ^ (1 / 2) / Val(vel)
                VR = Str(Abs(Val(YR)) / TR)
            End If
            
            
        End If
    
        If flagMode = 1 Then
            If Steps > 0 Then
                If Abs(Val(X1)) > Abs(Val(Y1)) Then
                    T1 = (Abs(Val(X1) ^ 2) + Abs(Val(Y1) ^ 2)) ^ (1 / 2) / Val(vel)
                    V1 = Str(Abs(Val(X1)) / T1)
                Else
                    T1 = (Abs(Val(X1) ^ 2) + Abs(Val(Y1) ^ 2)) ^ (1 / 2) / Val(vel)
                    V1 = Str(Abs(Val(Y1)) / T1)
                End If
            End If
            
            If Steps > 1 Then
                If Abs(Val(X2)) > Abs(Val(Y2)) Then
                    T2 = (Abs(Val(X2) ^ 2) + Abs(Val(Y2) ^ 2)) ^ (1 / 2) / Val(vel)
                    V2 = Str(Abs(Val(X2)) / T2)
                Else
                    T2 = (Abs(Val(X2) ^ 2) + Abs(Val(Y2) ^ 2)) ^ (1 / 2) / Val(vel)
                    V2 = Str(Abs(Val(Y2)) / T2)
                End If
            End If
                
            If Steps > 2 Then
                If Abs(Val(X3)) > Abs(Val(Y3)) Then
                    T3 = (Abs(Val(X3) ^ 2) + Abs(Val(Y3) ^ 2)) ^ (1 / 2) / Val(vel)
                    V3 = Str(Abs(Val(X3)) / T3)
                Else
                    T3 = (Abs(Val(X3) ^ 2) + Abs(Val(Y3) ^ 2)) ^ (1 / 2) / Val(vel)
                    V3 = Str(Abs(Val(Y3)) / T3)
                End If
            End If
                
            If Steps > 3 Then
                If Abs(Val(X4)) > Abs(Val(Y4)) Then
                    T4 = (Abs(Val(X4) ^ 2) + Abs(Val(Y4) ^ 2)) ^ (1 / 2) / Val(vel)
                    V4 = Str(Abs(Val(X4)) / T4)
                Else
                    T4 = (Abs(Val(X4) ^ 2) + Abs(Val(Y4) ^ 2)) ^ (1 / 2) / Val(vel)
                    V4 = Str(Abs(Val(Y4)) / T4)
                End If
            End If
            
            If Steps > 4 Then
                If Abs(Val(X5)) > Abs(Val(Y5)) Then
                    T5 = (Abs(Val(X5) ^ 2) + Abs(Val(Y5) ^ 2)) ^ (1 / 2) / Val(vel)
                    V5 = Str(Abs(Val(X5)) / T5)
                Else
                    T5 = (Abs(Val(X5) ^ 2) + Abs(Val(Y5) ^ 2)) ^ (1 / 2) / Val(vel)
                    V5 = Str(Abs(Val(Y5)) / T5)
                End If
            End If
            
            If Steps > 5 Then
                If Abs(Val(X6)) > Abs(Val(Y6)) Then
                    T6 = (Abs(Val(X6) ^ 2) + Abs(Val(Y6) ^ 2)) ^ (1 / 2) / Val(vel)
                    V6 = Str(Abs(Val(X6)) / T6)
                Else
                    T6 = (Abs(Val(X6) ^ 2) + Abs(Val(Y6) ^ 2)) ^ (1 / 2) / Val(vel)
                    V6 = Str(Abs(Val(Y6)) / T6)
                End If
            End If
        End If
        
    
        
        If flagMode = 2 Then
            
            If checkX = 1 Then
                If checkY = 0 Then
                    Tsingle = 2 * (Abs(Val(XR)) + Val(stepsize)) / Val(vel) + 2 * AddDelayTime / 1000
                    t = (Val(LN) * Tsingle) \ 1
                Else
                    Tsingle = (Val(XR) ^ 2 + Val(YR) ^ 2) ^ (1 / 2) / Val(vel) + 2 * AddDelayTime / 1000
                    t = (Val(LN) * Tsingle) \ 1
                End If
            ElseIf checkX = 0 Then
                If checkY = 1 Then
                    Tsingle = 2 * (Abs(Val(YR)) + Val(stepsize)) / Val(vel) + 2 * AddDelayTime / 1000
                    t = (Val(LN) * Tsingle) \ 1
                Else
                    Tsingle = 2 * (Abs(Val(XR)) + Abs(Val(YR))) / Val(vel) + 2 * AddDelayTime / 1000
                    t = (Val(LN) * Tsingle) \ 1
                End If
            
            End If
            
        End If
        
        If flagMode = 1 Then
            Tsingle = T1 + T2 + T3 + T4 + T5 + T6 + Steps * 0.02
            t = (Val(LN) * Tsingle) \ 1
        End If
        
        Timer1.Enabled = True
        flagStop = 0
        
        If flagMode = 3 Then
            Timer1.Enabled = False
        End If
        
        
        If t > 60 Then
            flagSound = 1
        Else
            flagSound = 0
        End If
        
        For i = 1 To Val(LN)
            If flagStop = 0 Then
                ypic.Cls
        
                ypic.Print i
                
                If flagMode = 2 Then
                
                    MoveRastor
                        
                ElseIf flagMode = 1 Then
            
                    MoveStageMovement
                    
                End If
            
    
            
'                If flagMode = 2 Then
'
'                    PauseTime = Tsingle
'                    Start = Timer
'                    Do While Timer < Start + PauseTime
'                        DoEvents
'                    Loop
'                    Finish = Timer
'
'                End If
            
            End If
        Next i
        
        
        
        ypic.Cls
        
        ypic.Print "end"
    End If
    
    If shutterIsOpen = True Then
        shutterClose
    End If
    
End Sub



'mode stage functions
'mode stage functions
'mode stage functions
'mode stage functions
'mode stage functions


Private Sub StageMovementSwitch_Click()
    
    If StageMovementSwitch.Caption = "Stage" Then
        StageMovementSwitch.Caption = "Laser Spot"
        flagStage = 0
    ElseIf StageMovementSwitch.Caption = "Laser Spot" Then
        StageMovementSwitch.Caption = "Stage"
        flagStage = 1
    End If

End Sub


Private Sub Go_Click()
    
    Label_SM_direction.Visible = True
    StageMovementSwitch.Visible = True

    
    If Val(Steps.Text) = 1 Then
        stage_frame1.Visible = True
        stage_frame2.Visible = False
        stage_frame3.Visible = False
        stage_frame4.Visible = False
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 2 Then
        
        
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = False
        stage_frame4.Visible = False
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
        
        
    ElseIf Val(Steps.Text) = 3 Then
        
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = False
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 4 Then
    
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = True
        stage_frame5.Visible = False
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 5 Then
    
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = True
        stage_frame5.Visible = True
        stage_frame6.Visible = False
        
    ElseIf Val(Steps.Text) = 6 Then
        
        stage_frame1.Visible = True
        stage_frame2.Visible = True
        stage_frame3.Visible = True
        stage_frame4.Visible = True
        stage_frame5.Visible = True
        stage_frame6.Visible = True
        
    End If

    If Val(Steps.Text) = 1 Then
        xinput2.Text = ""
        yinput2.Text = ""
        xinput3.Text = ""
        yinput3.Text = ""
        xinput4.Text = ""
        yinput4.Text = ""
        xinput5.Text = ""
        yinput5.Text = ""
        xinput6.Text = ""
        yinput6.Text = ""
    ElseIf Val(Steps.Text) = 2 Then
        xinput3.Text = ""
        yinput3.Text = ""
        xinput4.Text = ""
        yinput4.Text = ""
        xinput5.Text = ""
        yinput5.Text = ""
        xinput6.Text = ""
        yinput6.Text = ""
    ElseIf Val(Steps.Text) = 3 Then
        xinput4.Text = ""
        yinput4.Text = ""
        xinput5.Text = ""
        yinput5.Text = ""
        xinput6.Text = ""
        yinput6.Text = ""
    ElseIf Val(Steps.Text) = 4 Then
        xinput5.Text = ""
        yinput5.Text = ""
        xinput6.Text = ""
        yinput6.Text = ""
    ElseIf Val(Steps.Text) = 5 Then
        xinput6.Text = ""
        yinput6.Text = ""
    End If
    
 
End Sub






'Private Sub Text11_Change()
'
'    laserPrintContent = Text11.Text
''    Text12.Text = getbyte(laserPrintContent, 1)
''
'
'End Sub

Private Function getbyte(s As String, ByVal place As Integer) As String
    
    If place < Len(s) Then
        place = place + 1
        getbyte = Mid(s, place, 1)
    Else
        getbyte = ""
    End If
    
End Function

Private Sub correction_Change()

    testCorrection = correction.Text

End Sub

Private Sub Text14_Change()

    drawregioni = Text14.Text

End Sub





Private Sub Text2_Change()

    laserMotorFreq = Text2.Text

End Sub

Private Sub Text4_Change()

    If Text4.Text = "" Then
        Text4.Text = Text4.Text
    Else
        goToStepNum = Val(Text4.Text)
    End If
    
End Sub



Private Sub Text5_Change()

    If Text5.Text = "37914286" Then
        Advance_Option.Visible = True
        Advance_Pass.Visible = False
        Text5.Text = ""
    End If

End Sub

Private Sub Text6_Change()

    powerStepDelay = Text6.Text
    
End Sub



Private Sub Text9_Change()

    DrawPicExtraBoundry = Text9.Text

End Sub

Private Sub xinput1_Change()

    X1 = Str(Val(xinput1.Text) * -1)
    X1n = Str(Val(xinput1.Text))
    
End Sub

Private Sub yinput1_Change()
    
    Y1 = Str(Val(yinput1.Text) * -1)
    Y1n = Str(Val(yinput1.Text))
    
End Sub

Private Sub xinput2_Change()

    X2 = Str(Val(xinput2.Text) * -1)
    X2n = Str(Val(xinput2.Text))
    
End Sub

Private Sub yinput2_Change()
    
    Y2 = Str(Val(yinput2.Text) * -1)
    Y2n = Str(Val(xinput2.Text))
    
End Sub

Private Sub xinput3_Change()

    X3 = Str(Val(xinput3.Text) * -1)
    X3n = Str(Val(xinput3.Text))
    
End Sub

Private Sub yinput3_Change()

    Y3 = Str(Val(yinput3.Text) * -1)
    Y3n = Str(Val(yinput3.Text))
    
End Sub

Private Sub xinput4_Change()

    X4 = Str(Val(xinput4.Text) * -1)
    X4n = Str(Val(xinput4.Text))
    
End Sub

Private Sub yinput4_Change()

    Y4 = Str(Val(yinput4.Text) * -1)
    Y4n = Str(Val(yinput4.Text))
    
End Sub
Private Sub xinput5_Change()

    X5 = Str(Val(xinput5.Text) * -1)
    X5n = Str(Val(xinput5.Text))
    
End Sub

Private Sub yinput5_Change()
    
    Y5 = Str(Val(yinput5.Text) * -1)
    Y5n = Str(Val(yinput5.Text))
    
End Sub
Private Sub xinput6_Change()

    X6 = Str(Val(xinput6.Text) * -1)
    X6n = Str(Val(xinput6.Text))
    
End Sub

Private Sub yinput6_Change()

    Y6 = Str(Val(yinput6.Text) * -1)
    Y6n = Str(Val(yinput6.Text))
    
End Sub


Public Sub MoveStageMovement()

    sentV1 = V1 + "setvel" + enter
    sentV2 = V2 + "setvel" + enter
    sentV3 = V3 + "setvel" + enter
    sentV4 = V4 + "setvel" + enter
    sentV5 = V5 + "setvel" + enter
    sentV6 = V6 + "setvel" + enter
    l1 = X1 + blank + Y1 + blank + run + enter
    l2 = X2 + blank + Y2 + blank + run + enter
    l3 = X3 + blank + Y3 + blank + run + enter
    l4 = X4 + blank + Y4 + blank + run + enter
    l5 = X5 + blank + Y5 + blank + run + enter
    l6 = X6 + blank + Y6 + blank + run + enter
    l1n = X1n + blank + Y1n + blank + run + enter
    l2n = X2n + blank + Y2n + blank + run + enter
    l3n = X3n + blank + Y3n + blank + run + enter
    l4n = X4n + blank + Y4n + blank + run + enter
    l5n = X5n + blank + Y5n + blank + run + enter
    l6n = X6n + blank + Y6n + blank + run + enter
    
    If flagStage = 1 Then
        If Val(Steps.Text) > 0 Then
            MSComm1.Output = sentV1
            MSComm1.Output = l1
            positionX = positionX + X1
            positionY = positionY + Y1
            delay (T1)
        End If
            
        If Val(Steps.Text) > 1 Then
            MSComm1.Output = sentV2
            MSComm1.Output = l2
            positionX = positionX + X2
            positionY = positionY + Y2
            delay (T2)
        End If
             
        If Val(Steps.Text) > 2 Then
            MSComm1.Output = sentV3
            MSComm1.Output = l3
            positionX = positionX + X3
            positionY = positionY + Y3
            delay (T3)
        End If
        
        If Val(Steps.Text) > 3 Then
            MSComm1.Output = sentV4
            MSComm1.Output = l4
            positionX = positionX + X4
            positionY = positionY + Y4
            delay (T4)
        End If
            
        If Val(Steps.Text) > 4 Then
            MSComm1.Output = sentV1
            MSComm1.Output = l5
            positionX = positionX + X5
            positionY = positionY + Y5
            delay (T5)
        End If
         
        If Val(Steps.Text) > 5 Then
            MSComm1.Output = sentV6
            MSComm1.Output = l6
            positionX = positionX + X6
            positionY = positionY + Y6
            delay (T6)
        End If
    ElseIf flagStage = 0 Then
        If Val(Steps.Text) > 0 Then
            MSComm1.Output = sentV1
            MSComm1.Output = l1n
            positionX = positionX + X1n
            positionY = positionY + Y1n
            delay (T1)
        End If
            
        If Val(Steps.Text) > 1 Then
            MSComm1.Output = sentV2
            MSComm1.Output = l2n
            positionX = positionX + X2n
            positionY = positionY + Y2n
            delay (T2)
        End If
             
        If Val(Steps.Text) > 2 Then
            MSComm1.Output = sentV3
            MSComm1.Output = l3n
            positionX = positionX + X3n
            positionY = positionY + Y3n
            delay (T3)
        End If
        
        If Val(Steps.Text) > 3 Then
            MSComm1.Output = sentV4
            MSComm1.Output = l4n
            positionX = positionX + X4n
            positionY = positionY + Y4n
            delay (T4)
        End If
            
        If Val(Steps.Text) > 4 Then
            MSComm1.Output = sentV1
            MSComm1.Output = l5n
            positionX = positionX + X5n
            positionY = positionY + Y5n
            delay (T5)
        End If
         
        If Val(Steps.Text) > 5 Then
            MSComm1.Output = sentV6
            MSComm1.Output = l6n
            positionX = positionX + X6n
            positionY = positionY + Y6n
            delay (T6)
        End If
    End If

End Sub



'mode rastor functions
'mode rastor functions
'mode rastor functions
'mode rastor functions
'mode rastor functions


Private Sub xinputR_Change()

    XR = Str(Val(xinputR.Text))
    XRn = Str(Val(xinputR.Text) * -1)
    
    If flagMode = 2 Then
    
        If checkX = 0 Then
            If checkY = 1 Then
                XLoop.Text = Abs(XR) \ (2 * stepsize)
            End If
        End If
    
    End If
    ResetDelayTime
    
End Sub


Private Sub yinputR_Change()
    
    YR = Str(Val(yinputR.Text))
    YRn = Str(Val(yinputR.Text) * -1)
    
    If flagMode = 2 Then
        If checkX = 1 Then
            If checkY = 0 Then
                XLoop.Text = Abs(YR) \ (2 * stepsize)
            End If
        End If
    End If
    ResetDelayTime
    
End Sub


Private Sub rustX_Click()

    If rustX.Value = 1 Then
        checkX = 0
    Else
        checkX = 1
        
    End If
    
    If stepsize = "" Then
        step1.Text = 1
        step2.Text = 1
    End If
    
    If checkX = 0 Then
        If checkY = 0 Then
        
        step1.Visible = False
        Label53.Visible = False
        step2.Visible = False
        Label54.Visible = False
        Label55.Visible = False
        Label66.Visible = True
        Label56.Visible = False
        
        ElseIf checkY = 1 Then
        
        step1.Visible = True
        Label53.Visible = True
        step2.Visible = False
        Label54.Visible = False
        Label55.Visible = False
        Label66.Visible = False
        Label56.Visible = True
        step1.Text = stepsize
        
        End If
        
    ElseIf checkX = 1 Then
        
        If checkY = 0 Then
        
            step1.Visible = False
            Label53.Visible = False
            step2.Visible = True
            Label54.Visible = True
            Label55.Visible = False
            Label66.Visible = False
            Label56.Visible = True
            step2.Text = stepsize
        
        ElseIf checkY = 1 Then
        
            step1.Visible = False
            Label53.Visible = False
            step2.Visible = False
            Label54.Visible = False
            Label55.Visible = True
            Label66.Visible = False
            Label56.Visible = False
        
        End If
        
    End If
    
    
    If Val(stepsize) > 0 Then
        If checkX = 1 Then
            If checkY = 0 Then
                XLoop.Text = Abs(Val(YR)) \ (2 * Val(stepsize))
                
            Else
                XLoop.Text = 1
                
            End If
        ElseIf checkX = 0 Then
            If checkY = 1 Then
                XLoop.Text = Abs(Val(XR)) \ (2 * Val(stepsize))
            Else
                XLoop.Text = 1
            End If
        
        End If
    
    ElseIf Val(stepsize) = 0 Then
        XLoop.Text = 1
    
    End If
  
    watch1 = Val(LN)
    ResetDelayTime
    
End Sub


Private Sub rustY_Click()

    If rustY.Value = 1 Then
        checkY = 0
    Else
        checkY = 1
        
    End If
    
    If stepsize = "" Then
        step1.Text = 1
        step2.Text = 1
    End If
    
    If checkY = 0 Then
        If checkX = 0 Then
            
            step1.Visible = False
            Label53.Visible = False
            step2.Visible = False
            Label54.Visible = False
            Label55.Visible = False
            Label66.Visible = True
            Label56.Visible = False
        
        ElseIf checkX = 1 Then
        
            step1.Visible = False
            Label53.Visible = False
            step2.Visible = True
            Label54.Visible = True
            Label55.Visible = False
            Label66.Visible = False
            Label56.Visible = True
            step2.Text = stepsize
        
        End If
        
    ElseIf checkY = 1 Then
    
        If checkX = 0 Then
        
            step1.Visible = True
            Label53.Visible = True
            step2.Visible = False
            Label54.Visible = False
            Label55.Visible = False
            Label66.Visible = False
            Label56.Visible = True
            step1.Text = stepsize
            
        ElseIf checkX = 1 Then
        
            step1.Visible = False
            Label53.Visible = False
            step2.Visible = False
            Label54.Visible = False
            Label55.Visible = True
            Label66.Visible = False
            Label56.Visible = False
        
        End If
    End If
    
    
    
    
    
    If Val(stepsize) > 0 Then
        If checkX = 1 Then
            If checkY = 0 Then
                XLoop.Text = Abs(Val(YR)) \ (2 * Val(stepsize))

            Else
                XLoop.Text = 1
            End If
        ElseIf checkX = 0 Then
            If checkY = 1 Then
                XLoop.Text = Abs(Val(XR)) \ (2 * Val(stepsize))
            Else
                XLoop.Text = 1

            End If
        
        End If
    
    ElseIf Val(stepsize) = 0 Then
        XLoop.Text = 1
    
    End If
    
    watch1 = Val(LN)
    ResetDelayTime

End Sub





Private Sub step1_Change()

    stepsize = Str(Val(step1.Text))
    stepsizen = Str(Val(step1.Text) * -1)
    
    If Val(stepsize) > 0 Then
        If checkX = 1 Then
            If checkY = 0 Then
                XLoop.Text = Abs(Val(YR)) \ (2 * Val(stepsize))
            Else
                XLoop.Text = 1
            End If
        ElseIf checkX = 0 Then
            If checkY = 1 Then
                XLoop.Text = Abs(Val(XR)) \ (2 * Val(stepsize))
            Else
                XLoop.Text = 1
            End If
        
        End If
    
    ElseIf Val(stepsize) = 0 Then
        stepsize = Str(1)
        stepsizen = Str(-1)
    
    End If
    

End Sub



Private Sub step2_Change()

    stepsize = Str(Val(step2.Text))
    stepsizen = Str(Val(step2.Text) * -1)
    
    If Val(stepsize) > 0 Then
        If checkX = 1 Then
            If checkY = 0 Then
                XLoop.Text = Abs(Val(YR)) \ (2 * Val(stepsize))
            Else
                XLoop.Text = 1
            End If
        ElseIf checkX = 0 Then
            If checkY = 1 Then
                XLoop.Text = Abs(Val(XR)) \ (2 * Val(stepsize))
            Else
                XLoop.Text = 1
            End If
        
        End If

    
    ElseIf Val(stepsize) = 0 Then
        stepsize = Str(1)
        stepsizen = Str(-1)
    
    End If

End Sub


Public Sub ResetDelayTime()

    If checkX = 1 Then
        If checkY = 0 Then
            If Val(vel) > 0 Then
                AddDelayTime = Abs(Val(XR) / Val(vel) * 10)
                If AddDelayTime < 20 Then
                    AddDelayTime = 20
                ElseIf AddDelayTime > 5000 Then
                    AddDelayTime = 5000
                End If
            End If
        End If
    ElseIf checkY = 1 Then
        If checyx = 0 Then
            If Val(vel) > 0 Then
                AddDelayTime = Abs(Val(YR) / Val(vel) * 10)
                If AddDelayTime < 20 Then
                    AddDelayTime = 20
                ElseIf AddDelayTime > 5000 Then
                    AddDelayTime = 5000
                End If
            End If
        End If
    End If
    AddtionDelayTime.Text = AddDelayTime

End Sub

Public Sub MoveRastor()


    
    sentVR = VR + "setvel" + enter
    lr = XR + blank + YR + blank + run + enter
    lRx = XR + blank + zero + blank + run + enter
    lRy = zero + blank + YR + blank + run + enter
    lRxn = XRn + blank + zero + blank + run + enter
    lRyn = zero + blank + YRn + blank + run + enter
    lsx = stepsize + blank + zero + blank + run + enter
    lsy = zero + blank + stepsize + blank + run + enter
    lsxn = stepsizen + blank + zero + blank + run + enter
    lsyn = zero + blank + stepsizen + blank + run + enter

    If checkX = 1 Then
        If checkY = 0 Then
            If Val(YR) > 0 Then
    
                MSComm1.Output = lRx
                delayAccurate (Abs(Val(XR) / Val(vel) * 10000 + AddDelayTime * 10))
                MSComm1.Output = lsy
                delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                MSComm1.Output = lRxn
                delayAccurate (Abs(Val(XR) / Val(vel) * 10000 + AddDelayTime * 10))
                If i < Val(LN) Then
                    MSComm1.Output = lsy
                    delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                    positionX = positionX
                    positionY = positionY + 2 * stepsize
                Else
                    positionX = positionX
                    positionY = positionY + stepsize
                End If
            Else
                MSComm1.Output = lRx
                delayAccurate (Abs(Val(XR) / Val(vel) * 10000 + AddDelayTime * 10))
                MSComm1.Output = lsyn
                delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                MSComm1.Output = lRxn
                delayAccurate (Abs(Val(XR) / Val(vel) * 10000 + AddDelayTime * 10))
                If i < Val(LN) Then
                    MSComm1.Output = lsyn
                    positionX = positionX
                    delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                    positionY = positionY - 2 * stepsize
                Else
                    positionX = positionX
                    positionY = positionY + stepsize
                End If
            End If
        ElseIf checkY = 1 Then
            MSComm1.Output = sentVR
            MSComm1.Output = lr
            positionX = positionX + XR
            positionY = positionY + YR
        End If

    ElseIf checkX = 0 Then
        If checkY = 1 Then
            If Val(XR) > 0 Then
    
                MSComm1.Output = lRy
                delayAccurate (Abs(Val(YR) / Val(vel) * 10000 + AddDelayTime * 10))
                MSComm1.Output = lsx
                delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                MSComm1.Output = lRyn
                delayAccurate (Abs(Val(YR) / Val(vel) * 10000 + AddDelayTime * 10))
                If i < Val(LN) Then
                    MSComm1.Output = lsx
                    delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                    positionX = positionX + 2 * stepsize
                    positionY = positionY
                Else
                    positionX = positionX + stepsize
                    positionY = positionY
                End If
        
            Else
                MSComm1.Output = lRy
                delayAccurate (Abs(Val(YR) / Val(vel) * 10000 + AddDelayTime * 10))
                MSComm1.Output = lsxn
                delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                MSComm1.Output = lRyn
                delayAccurate (Abs(Val(YR) / Val(vel) * 10000 + AddDelayTime * 10))
                If i < Val(LN) Then
                    MSComm1.Output = lsxn
                    delayAccurate (Abs(Val(stepsize) / Val(vel) * 10000 + 200))
                    positionX = positionX - 2 * stepsize
                    positionY = positionY
                Else
                    positionX = positionX + stepsize
                    positionY = positionY
                End If
            End If
        ElseIf checkY = 0 Then
            MSComm1.Output = lRy
            MSComm1.Output = lRx
            MSComm1.Output = lRyn
            MSComm1.Output = lRxn
            positionX = positionX
            positionY = positionY
        End If
    End If
   
End Sub

Private Sub Command4_Click()
    positionY = positionY
End Sub

Public Sub MoveMultiRastorFun()

    Dim moveMultiI As Integer
    Dim positionI As Integer
    Dim waitingTime As Double
    Dim multiRowNum, multiColNum As Integer
    Dim spacingX, spacingY, totalSpacingX, totalSpacingY As Integer
    Dim maxDX, maxDY, maxSX, maxSY As Integer
    multiRowNum = CharNumOfRastor.Text
    multiColNum = CharNumOfRastor.Text
    maxDX = 0
    maxDY = 0
    maxSX = 0
    maxSY = 0
    totalSpacingX = 0
    totalSpacingY = 0
    For moveMultiI = 1 To totalMultiNum
    
        spacingX = multiR(moveMultiI).multiSX
        spacingY = multiR(moveMultiI).multiSY

        If multiR(moveMultiI).multiDX > maxDX Then
            maxDX = multiR(moveMultiI).multiDX
        End If
        If multiR(moveMultiI).multiDY > maxDY Then
            maxDY = multiR(moveMultiI).multiDY
        End If
        If multiR(moveMultiI).multiSX > maxSX Then
            maxSX = multiR(moveMultiI).multiSX
        End If
        If multiR(moveMultiI).multiSY > maxSY Then
            maxSY = multiR(moveMultiI).multiSY
        End If
            
        MultiRastorCurrentIndex.Text = moveMultiI
            
        SoundName$ = App.Path & "\sound\ding.wav"
        wFlags% = SND_ASYNC Or SND_NODEFAULT
        X% = sndPlaySound(SoundName$, wFlags%)
            
        Text4.Text = multiR(moveMultiI).multiPower
        Command1_Click
        waitingTime = multiR(moveMultiI).multiWaiting
        delayAccurate (waitingTime * 10000)
        
        If flagMultiOrder = 1 Then
        
            xinputR.Text = multiR(moveMultiI).multiDX
            yinputR.Text = -1 * multiR(moveMultiI).multiDY
            If multiR(moveMultiI).multiDirection = 1 Then
                
                rustX.Value = 1
                rustY.Value = 0
            
            ElseIf multiR(moveMultiI).multiDirection = 2 Then
            
                rustX.Value = 0
                rustY.Value = 1
            
            End If
            
            MoveStart_Click
            totalSpacingX = totalSpacingX + multiR(moveMultiI).multiDX
            
            If moveMultiI Mod multiRowNum = 0 Then
            
                moveToNext = Str(-1 * totalSpacingX) + blank + Str(-1 * (maxDY + maxSY)) + blank + run + enter
                MSComm1.Output = moveToNext
                waitingTime = (maxDY + maxSY) / Val(vel)
                delayAccurate (waitingTime * 10000)
                totalSpacingX = 0
                maxDY = 0
                maxSY = 0
'                waitingTime = multiR(moveMultiI).multiWaiting
'                delayAccurate (waitingTime * 10000)


            
            Else
            
                moveToNext = Str(spacingX) + blank + Str(0) + blank + run + enter
                MSComm1.Output = moveToNext
                totalSpacingX = totalSpacingX + spacingX
'                waitingTime = multiR(moveMultiI).multiWaiting
                waitingTime = spacingX / Val(vel)
                delayAccurate (waitingTime * 10000)
            
            End If
        
        ElseIf flagMultiOrder = 2 Then
        
            xinputR.Text = multiR(moveMultiI).multiDX
            yinputR.Text = -1 * multiR(moveMultiI).multiDY
            If multiR(moveMultiI).multiDirection = 1 Then
                
                rustX.Value = 1
                rustY.Value = 0
            
            ElseIf multiR(moveMultiI).multiDirection = 2 Then
            
                rustX.Value = 0
                rustY.Value = 1
            
            End If
            
            MoveStart_Click
            totalSpacingY = totalSpacingY + multiR(moveMultiI).multiDY
            
            If moveMultiI Mod multiRowNum = 0 Then
            
                moveToNext = Str(maxDX + maxSX) + blank + Str(totalSpacingY) + blank + run + enter
                MSComm1.Output = moveToNext
                waitingTime = (maxDX + maxSX) / Val(vel)
                delayAccurate (waitingTime * 10000)
                totalSpacingY = 0
                maxDX = 0
                maxSX = 0
'                waitingTime = multiR(moveMultiI).multiWaiting
'                delayAccurate (waitingTime * 10000)
            
            Else
            
                moveToNext = Str(0) + blank + Str(-1 * spacingY) + blank + run + enter
                MSComm1.Output = moveToNext
                totalSpacingY = totalSpacingY + spacingY
'                waitingTime = multiR(moveMultiI).multiWaiting
                waitingTime = spacingY / Val(vel)
                delayAccurate (waitingTime * 10000)
            End If
        
        End If
        
    Next

    SoundName$ = App.Path & "\sound\rastor.wav"
    wFlags% = SND_ASYNC Or SND_NODEFAULT
    X% = sndPlaySound(SoundName$, wFlags%)

End Sub

'arrow control mode functions
'arrow control mode functions
'arrow control mode functions
'arrow control mode functions
'arrow control mode functions


Private Sub AccuracyStep_Change()

    acStep = Val(AccuracyStep.Text)
    aM = Str(Val(AccuracyStep.Text))
    aMn = Str(Val(AccuracyStep.Text) * -1)
    If Val(vel) = 0 Then
        arrowStepTime = acStep / 100
    Else
        arrowStepTime = acStep / Val(vel)
    End If

End Sub


Private Sub origion_Click()

    positionX = 0
    positionY = 0
    WorldX = 0
    WorldY = 0
    arrowXpic.Cls
    
    arrowXpic.Cls
    
    arrowXpic.ForeColor = &HFF00&
    
    arrowXpic.Print positionX
    
    CorXV = positionX
    
    
    arrowYpic.Cls

    arrowYpic.ForeColor = &HFF00&

    arrowYpic.Print positionY
    
    CorYV = positionY

End Sub


Private Sub ArrowControlSwitch_Click()

    If ArrowControlSwitch.Caption = "Stage" Then
        ArrowControlSwitch.Caption = "Laser Spot"
        flagDisStage = 0
    ElseIf ArrowControlSwitch.Caption = "Laser Spot" Then
        ArrowControlSwitch.Caption = "Stage"
        flagDisStage = 1
    End If
    positionX = -1 * positionX
    positionY = -1 * positionY
    'circleXP = -1 * circleXP
    'circleYP = -1 * circleYP
    arrowXpic.Cls
    
    arrowXpic.ForeColor = &HFF00&
    
    arrowXpic.Print positionX
    
    CorXV = positionX
    
    
    arrowYpic.Cls

    arrowYpic.ForeColor = &HFF00&

    arrowYpic.Print positionY
    
    CorYV = positionY
    
    'CircleXpic.Cls
    
    'circleXpic.ForeColor = &HFF00&
    
    'circleXpic.Print circleXP
    
    
    'circleYpic.Cls

    'circleYpic.ForeColor = &HFF00&

    'circleYpic.Print circleYP
    

End Sub







'public functions: LoopNum, Velocity, timer, check zero, key down
'public functions: LoopNum, Velocity, timer, check zero, key down
'public functions: LoopNum, Velocity, timer, check zero, key down
'public functions: LoopNum, Velocity, timer, check zero, key down
'public functions: LoopNum, Velocity, timer, check zero, key down

Public Sub ArrowKeYDown(keycode, shift)

    If flagFirst = 1 Then
    sent = "-5000 -5000 5000 5000 setlimit" + enter
    Debug.Print sent
    MSComm1.Output = sent
    
    
    sent = "1 1 setunit" + enter ' x axis
    Debug.Print sent
    MSComm1.Output = sent
    
    sent = "1 2 setunit" + enter ' y axis
    Debug.Print sent
    MSComm1.Output = sent
    
    sent = "1 0 setunit" + enter ' velocity
    Debug.Print sent
    MSComm1.Output = sent
    
    flagFirst = 0
    End If
    sent = vel + "setvel" + enter
    Debug.Print sent
    MSComm1.Output = sent
    
    
    
    lus = zero + blank + aMn + blank + run + enter
    lds = zero + blank + aM + blank + run + enter
    lls = aM + blank + zero + blank + run + enter
    lrs = aMn + blank + zero + blank + run + enter
    lul = zero + blank + aM + blank + run + enter
    ldl = zero + blank + aMn + blank + run + enter
    lll = aMn + blank + zero + blank + run + enter
    lrl = aM + blank + zero + blank + run + enter
    
    
    If flagDelay = 1 Then
    flagDelay = 0
    
    If flagDisStage = 1 Then
        Select Case keycode
        
            Case vbKeyUp
                positionY = positionY + acStep
                'circleYP = circleYP + acStep
                MSComm1.Output = lus
                flagArrowKey = 1
                WorldY = WorldY + 1
            Case vbKeyDown
                positionY = positionY - acStep
                'circleYP = circleYP - acStep
                MSComm1.Output = lds
                flagArrowKey = 1
                WorldY = WorldY - 1
            Case vbKeyLeft
                positionX = positionX - acStep
                'circleXP = circleXP - acStep
                MSComm1.Output = lls
                flagArrowKey = 1
                WorldX = WorldX - 1
            Case vbKeyRight
                positionX = positionX + acStep
                'circleXP = circleXP + acStep
                MSComm1.Output = lrs
                flagArrowKey = 1
                WorldX = WorldX + 1
        
        End Select
    ElseIf flagDisStage = 0 Then
        Select Case keycode
        
            Case vbKeyUp
                positionY = positionY + acStep
                'circleYP = circleYP + acStep
                MSComm1.Output = lul
                flagArrowKey = 1
                WorldY = WorldY - 1
            Case vbKeyDown
                positionY = positionY - acStep
                'circleYP = circleYP - acStep
                MSComm1.Output = ldl
                flagArrowKey = 1
                WorldY = WorldY + 1
            Case vbKeyLeft
                positionX = positionX - acStep
                'circleXP = circleXP - acStep
                MSComm1.Output = lll
                flagArrowKey = 1
                WorldX = WorldX + 1
            Case vbKeyRight
                positionX = positionX + acStep
                'circleXP = circleXP + acStep
                MSComm1.Output = lrl
                flagArrowKey = 1
                WorldX = WorldX - 1
        
        End Select
    End If
    
    arrowXpic.Cls
    
    arrowXpic.ForeColor = &HFF&
    
    arrowXpic.Print positionX
    
    
    
    
    arrowYpic.Cls
    
    arrowYpic.ForeColor = &HFF&
    
    arrowYpic.Print positionY
    
    
    If flagArrowKey = 1 Then
        CorXV = positionX
    
        CorYV = positionY
    End If
    
    'circleXpic.Cls
    
    'circleXpic.ForeColor = &HFF&
    
    'circleXpic.Print circleXP
    
    'circleYpic.Cls
    
    'circleYpic.ForeColor = &HFF&
    
    'circleYpic.Print circleYP
    
    
    
    t = 0.02 + arrowStepTime
    If t > 1 Then
        Timer1.Enabled = True
    
        If t > 60 Then
            flagSound = 1
        Else
            flagSound = 0
        End If
        
    Else
        flagSound = 0
    End If
    
    If flagArrowKey = 1 Then
        flagArrowKey = 0
        'tempRadius = Round((circleXP ^ 2 + circleYP ^ 2) ^ (1 / 2), 2)
        'radius.Text = Str(tempRadius)
        PauseTime = 0.02 + arrowStepTime
        Start = Timer
        Do While Timer < Start + PauseTime
            DoEvents
        Loop
        Finish = Timer
    End If
    
    arrowXpic.Cls
    
    arrowXpic.ForeColor = &HFF00&
    
    arrowXpic.Print positionX
    
    
    
    arrowYpic.Cls
    
    arrowYpic.ForeColor = &HFF00&
    
    arrowYpic.Print positionY
    
    If flagArrowKey = 1 Then
        CorXV = positionX
    
        CorYV = positionY
    End If
    
    
    'circleXpic.Cls
    
    'circleXpic.ForeColor = &HFF00&
    
    'circleXpic.Print circleXP
    
    
    'circleYpic.Cls
    
    'circleYpic.ForeColor = &HFF00&
    
    'circleYpic.Print circleYP
    
    
    flagDelay = 1
    
    End If

End Sub


Private Sub Form_KeyDown(keycode As Integer, shift As Integer)
    
    Dim startThisX, startThisY, endThisX, endThisY As Integer
    
    
'        If KeyCode = vbKeyA Then
'            If Shift = 1 Then
'                Text5.Text = "success"
'            End If
'        End If
'   pageup=33, pagedown=34, home=36, end=35
'    Text2.Text = keycode
    If allowPowerChange = True Then
        If flagMode < 6 Then
            Select Case keycode
                
                Case vbKeyF1
                    If shutterIsOpen = False Then
                        Laser_Open_Click
                    ElseIf shutterIsOpen = True Then
                        Laser_Close_Click
                    End If
    
                
                Case 33
                    StepFreq = laserMotorFreq * 8
                    If Check1.Value = 1 Then
                        For i = 1 To laserStep
                            out Val("&H378"), Val(100)
                            delayAccurate (1 / StepFreq * 10000)
                            out Val("&H378"), Val(0)
                            delayAccurate (1 / StepFreq * 10000)
                        Next
                        laserPosition = laserPosition + laserStep * 1.8 / 8
                        totalStep = totalStep + laserStep / 8
                        CurrentAngle.Text = laserPosition
                        Text3.Text = totalStep
                    ElseIf Check1.Value = 0 Then
                        If Text3.Text + MotorStep.Text < 1951 Then
                            For i = 1 To laserStep
                                out Val("&H378"), Val(100)
                                delayAccurate (1 / StepFreq * 10000)
                                out Val("&H378"), Val(0)
                                delayAccurate (1 / StepFreq * 10000)
                            Next
                            laserPosition = laserPosition + laserStep * 1.8 / 8
                            totalStep = totalStep + laserStep / 8
                            CurrentAngle.Text = laserPosition
                            Text3.Text = totalStep
                        ElseIf Text3.Text + MotorStep.Text > 1950 Then
                            goToStepNum = 1950
                            adjustLaser
                        End If
                        
                    End If
                    allowPowerChange = False
                    
                Case 34
                    StepFreq = laserMotorFreq * 8
                    If Check1.Value = 1 Then
                        For i = 1 To laserStep
                            out Val("&H378"), Val(1100)
                            delayAccurate (1 / StepFreq * 10000)
                            out Val("&H378"), Val(1000)
                            delayAccurate (1 / StepFreq * 10000)
                        Next
                        
                        laserPosition = laserPosition - laserStep * 1.8 / 8
                        totalStep = totalStep - laserStep / 8
                        CurrentAngle.Text = laserPosition
                        Text3.Text = totalStep
                    ElseIf Check1.Value = 0 Then
                        If Text3.Text - MotorStep.Text > -1 Then
                            For i = 1 To laserStep
                                out Val("&H378"), Val(1100)
                                delayAccurate (1 / StepFreq * 10000)
                                out Val("&H378"), Val(1000)
                                delayAccurate (1 / StepFreq * 10000)
                            Next
                            
                            laserPosition = laserPosition - laserStep * 1.8 / 8
                            totalStep = totalStep - laserStep / 8
                            CurrentAngle.Text = laserPosition
                            Text3.Text = totalStep
                        ElseIf Text3.Text - MotorStep.Text < 0 Then
                            goToStepNum = 0
                            adjustLaser
                        End If
                    End If
                    allowPowerChange = False
                
                Case 36
                    StepFreq = laserMotorFreq * 8
                    goToStepNum = 0
                    adjustLaser
                
                Case 35
                    StepFreq = laserMotorFreq * 8
                    goToStepNum = 1950
                    adjustLaser
                    
            End Select
            
        End If
        If allowPowerChange = False Then
            If Check1.Value = 0 Then
                delayAccurate (powerStepDelay)
            End If
            allowPowerChange = True
        End If
        
    End If
    
    If flagMode = 3 Then
        Call ArrowKeYDown(keycode, shift)
'    ElseIf flagMode = 4 Then
'
'        Select Case keycode
'
'            Case vbKeyUp
'                For I = 1 To laserStep
'                    out Val("&H378"), Val(100)
'                    delayAccurate (1 / StepFreq * 10000)
'                    out Val("&H378"), Val(0)
'                    delayAccurate (1 / StepFreq * 10000)
'                Next
'                laserPosition = laserPosition + laserStep * 1.8 / 8
'                totalStep = totalStep + laserStep / 8
'                CurrentAngle.Text = laserPosition
'                Text3.Text = totalStep
'
'            Case vbKeyDown
'
'                For I = 1 To laserStep
'                    out Val("&H378"), Val(1100)
'                    delayAccurate (1 / StepFreq * 10000)
'                    out Val("&H378"), Val(1000)
'                    delayAccurate (1 / StepFreq * 10000)
'                Next
'
'                laserPosition = laserPosition - laserStep * 1.8 / 8
'                totalStep = totalStep - laserStep / 8
'                CurrentAngle.Text = laserPosition
'                Text3.Text = totalStep
'
'        End Select
    ElseIf flagMode = 5 Then
    
        picRegionMax = 200
        picRegionMin = -1
        picDrawCorrect = 130
        If printType1 = True Then
            If flagPrintEnd = True Then
                Select Case keycode
    '                Case vbKey1
    '                    Open (App.Path & "\font\1.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey2
    '                    Open (App.Path & "\font\2.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey3
    '                    Open (App.Path & "\font\3.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey4
    '                    Open (App.Path & "\font\4.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey5
    '                    Open (App.Path & "\font\5.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey6
    '                    Open (App.Path & "\font\6.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey7
    '                    Open (App.Path & "\font\7.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey8
    '                    Open (App.Path & "\font\8.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey9
    '                    Open (App.Path & "\font\9.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
    '                Case vbKey0
    '                    Open (App.Path & "\font\0.bmp") For Binary As #1
    '                    flagPrintEnd = False
    '                    input_picinfo
    '                    drawRegion
    '                    flagPrintEnd = True
                    Case vbKeyA
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 1)
                        Else
                            Call drawFont(2, 1)
                        End If
                        flagPrintEnd = True
                    Case vbKeyB
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 2)
                        Else
                            Call drawFont(2, 2)
                        End If
                        flagPrintEnd = True
                    Case vbKeyC
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 3)
                        Else
                            Call drawFont(2, 3)
                        End If
                        flagPrintEnd = True
                    Case vbKeyD
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 4)
                        Else
                            Call drawFont(2, 4)
                        End If
                        flagPrintEnd = True
                    Case vbKeyE
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 5)
                        Else
                            Call drawFont(2, 5)
                        End If
                        flagPrintEnd = True
                    Case vbKeyF
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 6)
                        Else
                            Call drawFont(2, 6)
                        End If
                        flagPrintEnd = True
                    Case vbKeyG
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 7)
                        Else
                            Call drawFont(2, 7)
                        End If
                        flagPrintEnd = True
                    Case vbKeyH
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 8)
                        Else
                            Call drawFont(2, 8)
                        End If
                        flagPrintEnd = True
                    Case vbKeyI
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 9)
                        Else
                            Call drawFont(2, 9)
                        End If
                        flagPrintEnd = True
                    Case vbKeyJ
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 10)
                        Else
                            Call drawFont(2, 10)
                        End If
                        flagPrintEnd = True
                    Case vbKeyK
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 11)
                        Else
                            Call drawFont(2, 11)
                        End If
                        flagPrintEnd = True
                    Case vbKeyL
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 12)
                        Else
                            Call drawFont(2, 12)
                        End If
                        flagPrintEnd = True
                    Case vbKeyM
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(4, 13)
                        Else
                            Call drawFont(2, 13)
                        End If
                        flagPrintEnd = True
                    Case vbKeyN
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 1)
                        Else
                            Call drawFont(3, 1)
                        End If
                        flagPrintEnd = True
                    Case vbKeyO
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 2)
                        Else
                            Call drawFont(3, 2)
                        End If
                        flagPrintEnd = True
                    Case vbKeyP
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 3)
                        Else
                            Call drawFont(3, 3)
                        End If
                        flagPrintEnd = True
                    Case vbKeyQ
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 4)
                        Else
                            Call drawFont(3, 4)
                        End If
                        flagPrintEnd = True
                    Case vbKeyR
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 5)
                        Else
                            Call drawFont(3, 5)
                        End If
                        flagPrintEnd = True
                    Case vbKeyS
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 6)
                        Else
                            Call drawFont(3, 6)
                        End If
                        flagPrintEnd = True
                    Case vbKeyT
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 7)
                        Else
                            Call drawFont(3, 7)
                        End If
                        flagPrintEnd = True
                    Case vbKeyU
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 8)
                        Else
                            Call drawFont(3, 8)
                        End If
                        flagPrintEnd = True
                    Case vbKeyV
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 9)
                        Else
                            Call drawFont(3, 9)
                        End If
                        flagPrintEnd = True
                    Case vbKeyW
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 10)
                        Else
                            Call drawFont(3, 10)
                        End If
                        flagPrintEnd = True
                    Case vbKeyX
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 11)
                        Else
                            Call drawFont(3, 11)
                        End If
                        flagPrintEnd = True
                    Case vbKeyY
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 12)
                        Else
                            Call drawFont(3, 12)
                        End If
                        flagPrintEnd = True
                    Case vbKeyZ
                        flagPrintEnd = False
                        If shift = 1 Then
                            Call drawFont(5, 13)
                        Else
                            Call drawFont(3, 13)
                        End If
                        flagPrintEnd = True
                    Case vbKey0
                        flagPrintEnd = False
                        Call drawFont(1, 10)
                        flagPrintEnd = True
                    Case vbKey1
                        flagPrintEnd = False
                        Call drawFont(1, 1)
                        flagPrintEnd = True
                    Case vbKey2
                        flagPrintEnd = False
                        Call drawFont(1, 2)
                        flagPrintEnd = True
                    Case vbKey3
                        flagPrintEnd = False
                        Call drawFont(1, 3)
                        flagPrintEnd = True
                    Case vbKey4
                        flagPrintEnd = False
                        Call drawFont(1, 4)
                        flagPrintEnd = True
                    Case vbKey5
                        flagPrintEnd = False
                        Call drawFont(1, 5)
                        flagPrintEnd = True
                    Case vbKey6
                        flagPrintEnd = False
                        Call drawFont(1, 6)
                        flagPrintEnd = True
                    Case vbKey7
                        flagPrintEnd = False
                        Call drawFont(1, 7)
                        flagPrintEnd = True
                    Case vbKey8
                        flagPrintEnd = False
                        Call drawFont(1, 8)
                        flagPrintEnd = True
                    Case vbKey9
                        flagPrintEnd = False
                        Call drawFont(1, 9)
                        flagPrintEnd = True
                    Case vbKeySubtract
                        flagPrintEnd = False
                        Call drawFont(1, 11)
                        flagPrintEnd = True
                    Case vbKeyAdd
                        flagPrintEnd = False
                        Call drawFont(1, 12)
                        flagPrintEnd = True
                    Case vbKeyDecimal
                        flagPrintEnd = False
                        Call drawFont(1, 13)
                        flagPrintEnd = True
                    Case 189
                        flagPrintEnd = False
                        Call drawFont(1, 11)
                        flagPrintEnd = True
                    Case 187
                        flagPrintEnd = False
                        Call drawFont(1, 12)
                        flagPrintEnd = True
                    Case 190
                        flagPrintEnd = False
                        Call drawFont(1, 13)
                        flagPrintEnd = True
                End Select
            End If
        End If
        Call ArrowKeYDown(keycode, shift)
    End If
    

End Sub


Private Sub velocity_Change()

    vel = Str(Val(velocity.Text))
    If Val(vel) = 0 Then
        arrowStepTime = acStep / 100
    Else
        arrowStepTime = acStep / Val(vel)
    End If
    If flagMode = 2 Then
        ResetDelayTime
    End If
    
End Sub


Private Sub XLoop_Change()

    LN = Str(Val(XLoop.Text))
    If flagMode = 2 Then
        If Val(LN) > 0 Then
            If checkX = 0 Then
                If checkY = 1 Then
                    If xinputR.Text < 0 Then
                        xinputR.Text = -2 * stepsize * Val(LN)
                    Else
                        xinputR.Text = 2 * stepsize * Val(LN)
                    End If
                End If
            ElseIf checkX = 1 Then
                If checkY = 0 Then
                    If yinputR.Text < 0 Then
                        yinputR.Text = -2 * stepsize * Val(LN)
                    Else
                        yinputR.Text = 2 * stepsize * Val(LN)
                    End If
                End If
            End If
        End If
    
    End If

End Sub


Private Sub Timer1_Timer()

     If (t < 2) Then
        Timer1.Enabled = False
    End If
    
    If t = 20 Then
    
        If flagSound = 1 Then
            SoundName$ = App.Path & "\sound\rastor.wav"
            wFlags% = SND_ASYNC Or SND_NODEFAULT
            X% = sndPlaySound(SoundName$, wFlags%)
        End If
        
    End If
    
   
    t = t - 1
    
    
    sec = t Mod 60
    min = (t \ 60) Mod 60
    hour = (t \ 60) \ 60
 
    
        
End Sub


Public Sub checkZeroFix()

    Dim flagStageStepRenew As Integer
    Dim flagBothZero As Integer
    Dim stageTempXY(1 To 6, 1 To 2) As Integer
    Dim stagei As Integer
    stagei = 1
    flagBothZero = 0
    flagStageStepRenew = 0
    If flagMode = 1 Then
        If Val(Steps.Text) > 0 Then
            If Val(xinput1.Text) = 0 Then
                xinput1.Text = 0
                flagBothZero = 1
            End If
            If Val(yinput1.Text) = 0 Then
                yinput1.Text = 0
                If flagBothZero = 1 Then
                    flagBothZero = 2
                    flagStageStepRenew = flagStageStepRenew + 1
                End If
            End If
            If flagBothZero < 2 Then
                stageTempXY(stagei, 1) = Val(xinput1.Text)
                stageTempXY(stagei, 2) = Val(yinput1.Text)
                stagei = stagei + 1
            End If
            flagBothZero = 0
        End If
        If Val(Steps.Text) > 1 Then
            If Val(xinput2.Text) = 0 Then
                xinput2.Text = 0
                flagBothZero = 1
            End If
            If Val(yinput2.Text) = 0 Then
                yinput2.Text = 0
                If flagBothZero = 1 Then
                    flagBothZero = 2
                    flagStageStepRenew = flagStageStepRenew + 1
                End If
            End If
            If flagBothZero < 2 Then
                stageTempXY(stagei, 1) = Val(xinput2.Text)
                stageTempXY(stagei, 2) = Val(yinput2.Text)
                stagei = stagei + 1
            End If
            flagBothZero = 0
        End If
        If Val(Steps.Text) > 2 Then
            If Val(xinput3.Text) = 0 Then
                xinput3.Text = 0
                flagBothZero = 1
            End If
            If Val(yinput3.Text) = 0 Then
                yinput3.Text = 0
                If flagBothZero = 1 Then
                    flagBothZero = 2
                    flagStageStepRenew = flagStageStepRenew + 1
                End If
            End If
            If flagBothZero < 2 Then
                stageTempXY(stagei, 1) = Val(xinput3.Text)
                stageTempXY(stagei, 2) = Val(yinput3.Text)
                stagei = stagei + 1
            End If
            flagBothZero = 0
        End If
        If Val(Steps.Text) > 3 Then
            If Val(xinput4.Text) = 0 Then
                xinput4.Text = 0
                flagBothZero = 1
                
            End If
            If Val(yinput4.Text) = 0 Then
                yinput4.Text = 0
                If flagBothZero = 1 Then
                    flagBothZero = 2
                    flagStageStepRenew = flagStageStepRenew + 1
                End If
            End If
            If flagBothZero < 2 Then
                stageTempXY(stagei, 1) = Val(xinput4.Text)
                stageTempXY(stagei, 2) = Val(yinput4.Text)
                stagei = stagei + 1
            End If
            flagBothZero = 0
        End If
        If Val(Steps.Text) > 4 Then
            If Val(xinput5.Text) = 0 Then
                xinput5.Text = 0
                flagBothZero = 1
            End If
            If Val(yinput5.Text) = 0 Then
                yinput5.Text = 0
                If flagBothZero = 1 Then
                    flagBothZero = 2
                    flagStageStepRenew = flagStageStepRenew + 1
                End If
            End If
            If flagBothZero < 2 Then
                stageTempXY(stagei, 1) = Val(xinput5.Text)
                stageTempXY(stagei, 2) = Val(yinput5.Text)
                stagei = stagei + 1
            End If
            flagBothZero = 0
        End If
        If Val(Steps.Text) > 5 Then
            If Val(xinput6.Text) = 0 Then
                xinput6.Text = 0
                flagBothZero = 1
            End If
            If Val(yinput6.Text) = 0 Then
                yinput6.Text = 0
                If flagBothZero = 1 Then
                    flagBothZero = 2
                    flagStageStepRenew = flagStageStepRenew + 1
                End If
            End If
            If flagBothZero < 2 Then
                stageTempXY(stagei, 1) = Val(xinput6.Text)
                stageTempXY(stagei, 2) = Val(yinput6.Text)
                stagei = stagei + 1
            End If
            flagBothZero = 0
        End If
        
        If flagStageStepRenew > 0 Then
            xinput1.Text = ""
            yinput1.Text = ""
            xinput2.Text = ""
            yinput2.Text = ""
            xinput3.Text = ""
            yinput3.Text = ""
            xinput4.Text = ""
            yinput4.Text = ""
            xinput5.Text = ""
            yinput5.Text = ""
            xinput6.Text = ""
            yinput6.Text = ""
            stage_frame1.Visible = False
            stage_frame2.Visible = False
            stage_frame3.Visible = False
            stage_frame4.Visible = False
            stage_frame5.Visible = False
            stage_frame6.Visible = False
            Steps.Text = Val(Steps.Text) - flagStageStepRenew
            If Steps.Text > 0 Then
                xinput1 = Str(stageTempXY(1, 1))
                yinput1 = Str(stageTempXY(1, 2))
                stage_frame1.Visible = True
            End If
            If Steps.Text > 1 Then
                xinput2 = Str(stageTempXY(2, 1))
                yinput2 = Str(stageTempXY(2, 2))
                stage_frame2.Visible = True
            End If
            If Steps.Text > 2 Then
                xinput3 = Str(stageTempXY(3, 1))
                yinput3 = Str(stageTempXY(3, 2))
                stage_frame3.Visible = True
            End If
            If Steps.Text > 3 Then
                xinput4 = Str(stageTempXY(4, 1))
                yinput4 = Str(stageTempXY(4, 2))
                stage_frame4.Visible = True
            End If
            If Steps.Text > 4 Then
                xinput5 = Str(stageTempXY(5, 1))
                yinput5 = Str(stageTempXY(5, 2))
                stage_frame5.Visible = True
            End If
                
            
        End If
    End If
    

End Sub


Public Sub checkZeroWarning()

    flagWarning = 0
    If Val(velocity.Text) = 0 Then
        WarningText.Caption = "Please input the velocity"
        showWarning
        flagWarning = 1
    End If
    
    If flagMode = 1 Then
        If Val(Steps.Text) = 0 Then
            WarningText.Caption = "Please set steps"
            showWarning
            flagWarning = 1
        End If
    End If
    
    If flagMode = 2 Then
        
        If Val(xinputR.Text) = 0 Then
            WarningText.Caption = "Please input parameters"
            showWarning
            flagWarning = 1
        End If
        If Val(yinputR.Text) = 0 Then
            WarningText.Caption = "Please input parameters"
            showWarning
            flagWarning = 1
        End If
        If Val(step1.Text) = 0 Then
            If Val(step2.Text) = 0 Then
                WarningText.Caption = "Please input parameters"
                showWarning
                flagWarning = 1
            End If
        End If
        
    End If

End Sub


Public Sub showWarning()

    Warning_frame.Top = 3000
    Warning_frame.Left = 1800
    Warning_frame.Height = 975
    Warning_frame.Width = 2895
    Warning_frame.Visible = True

End Sub

Private Sub CloseWarning_Click()

    Warning_frame.Visible = False

End Sub





'time control functions
'time control functions
'time control functions
'time control functions
'time control functions


'Private Sub testTimeComd_Click()
'
'    debugText.Text = "start"
'    For j = 1 To 10
'        For I = 1 To 20000
'
'            delay (2)
'
'        Next
'        watchi.Text = j
'    Next
'    debugText.Text = "end"
'End Sub

Public Sub delay(delayTime As Double)

    Start = Timer
    Do While Timer < Start + delayTime + 0.02
        DoEvents
    Loop
    Finish = Timer

End Sub



'Public Sub delay(ByVal num As Integer)
'
'Dim t As Long
't = timeGetTime
'Do Until timeGetTime - t >= num
'DoEvents
'Loop
'
'End Sub
'resolution is 10ms



'freq=3579545
Public Sub delayAccurate(delayNum As Double)
    Dim ctr1, ctr2, Freq As Currency
    
    If QueryPerformanceFrequency(Freq) Then
        QueryPerformanceCounter ctr1
        Do
            DoEvents
            QueryPerformanceCounter ctr2
        Loop While (ctr2 - ctr1) / Freq * 10000 < delayNum
    End If
        
    
End Sub




'Step motor functions
'Step motor functions
'Step motor functions
'Step motor functions
'Step motor functions


Private Sub StopStep_Click()

    flagStopStep = 1

End Sub

Private Sub testFinal_Click()

    vel = Str(1000)
    X1 = Str(0)
    Y1 = Str(500)
    
    sent = "-5000 -5000 5000 5000 setlimit" + enter
    Debug.Print sent
    MSComm1.Output = sent
    
    
    
    sent = "1 1 setunit" + enter ' x axis
    Debug.Print sent
    MSComm1.Output = sent
    
    sent = "1 2 setunit" + enter ' y axis
    Debug.Print sent
    MSComm1.Output = sent
    
    sent = "1 0 setunit" + enter ' velocity
    Debug.Print sent
    MSComm1.Output = sent

    sent = vel + "setvel" + enter
    Debug.Print sent
    MSComm1.Output = sent
    
    l1 = X1 + blank + Y1 + blank + run + enter
    
    
    
    MSComm1.Output = l1
    
    delayAccurate (5000)
    
    
    
    out Val("&H378"), Val(1)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(0)
    delayAccurate (1 / StepFreq * 10000)

    
End Sub

Private Sub TestStep_Click()

    flagStopStep = 0
    'Do While flagStopStep = 0
    For i = 1 To 3200
        out Val("&H378"), Val(11)
        delayAccurate (1 / StepFreq * 10000)
        out Val("&H378"), Val(0)
        delayAccurate (1 / StepFreq * 10000)
    Next
    'Loop
        

End Sub

Private Sub TestStepAnother_Click()

    out Val("&H378"), Val(11)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(10)
    delayAccurate (1 / StepFreq * 10000)

End Sub

Private Sub TestStepOne_Click()

    out Val("&H378"), Val(1)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(0)
    delayAccurate (1 / StepFreq * 10000)

End Sub

Private Sub TestStepShake_Click()

    out Val("&H378"), Val(11)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(10)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(1)
    delayAccurate (1 / StepFreq * 10000)
    out Val("&H378"), Val(0)
    delayAccurate (1 / StepFreq * 10000)
    

End Sub



'for laser control function
'for laser control function
'for laser control function
'for laser control function
'for laser control function

Private Sub MotorStep_Change()

    If MotorStep.Text = "" Then
        MotorStep.Text = MotorStep.Text
    Else
        laserStep = Val(MotorStep.Text) * 8
    End If

End Sub

Private Sub flag_laser_Click()

    flagMode = 4
    StageControl.KeyPreview = True
    StepFreq = 1500 * 8
End Sub











'for drawing circle, unused
'for drawing circle, unused
'for drawing circle, unused
'for drawing circle, unused
'for drawing circle, unused


'Private Sub radius_Change()
'
'    tempRadius = Str(Val(radius.Text))
'    flagStartingPoint = 0
'    CircleInfo.Cls
'    CircleInfo.Print "    Click to move to starting point. Keep laser closed."
'
'End Sub
'
'Private Sub SetCor_Click()
'
'    If CorXV = "" Then
'        CorXV = 0
'    End If
'
'    If CorYV = "" Then
'        CorYV = 0
'    End If
'
'    positionX = CorXV
'
'    positionY = CorYV
'
'     arrowXpic.Cls
'
'    arrowXpic.ForeColor = &HFF00&
'
'    arrowXpic.Print positionX
'
'
'    arrowYpic.Cls
'
'    arrowYpic.ForeColor = &HFF00&
'
'    arrowYpic.Print positionY
'
'    CorYV = positionY
'End Sub
'
'Private Sub SetEdge_Click()
'
'    flagStartingPoint = 0
'    CircleInfo.Cls
'    CircleInfo.Print "    Click to move to starting point. Keep laser closed."
'
'    CurrentRadius = tempRadius
'    radiuspic.Cls
'    radiuspic.Print CurrentRadius
'
'End Sub
'
'Private Sub SetOrigion_Click()
'
'    circleXP = 0
'    circleYP = 0
'    flagStartingPoint = 0
'    CircleInfo.Cls
'    CircleInfo.Print "    Click to move to starting point. Keep laser closed."
'
'    CircleXpic.Cls
'
'    CircleXpic.ForeColor = &HFF00&
'
'    CircleXpic.Print circleXP
'
'
'    CircleYpic.Cls
'
'    CircleYpic.ForeColor = &HFF00&
'
'    CircleYpic.Print circleYP
'
'    tempRadius = Round((circleXP ^ 2 + circleYP ^ 2) ^ (1 / 2), 2)
'    radius.Text = Str(tempRadius)
'
'End Sub
'
'
'
'Private Sub SetRadius_Click()
'
'    flagStartingPoint = 0
'    CircleInfo.Cls
'    CircleInfo.Print "    Click to move to starting point. Keep laser closed."
'
'    CurrentRadius = tempRadius
'    radiuspic.Cls
'    radiuspic.Print CurrentRadius
'
'End Sub


'Private Sub StartCircle_Click()
'
'    sent = "-5000 -5000 5000 5000 setlimit" + enter
'    Debug.Print sent
'    MSComm1.Output = sent
'
'
'    sent = "1 1 setunit" + enter ' x axis
'    Debug.Print sent
'    MSComm1.Output = sent
'
'    sent = "1 2 setunit" + enter ' y axis
'    Debug.Print sent
'    MSComm1.Output = sent
'
'    sent = "1 0 setunit" + enter ' velocity
'    Debug.Print sent
'    MSComm1.Output = sent
'
'    sent = vel + "setvel" + enter
'    Debug.Print sent
'    MSComm1.Output = sent
'
'    If flagDisStage = 1 Then
'        circleXP = -1 * circleXP
'        circleYP = -1 * circleYP
'    End If
'
'
'    DrawRadius = CurrentRadius \ 1
'    t = 0
'    TcircleXP = circleXP
'    TcircleYP = circleYP
'    For i = -1 * DrawRadius To DrawRadius Step 1
'        If Abs(i) = DrawRadius Then
'            TcircleAimX = i
'            TcircleAimY = 0
'        Else
'            TcircleAimX = i
'            TcircleAimY = (CurrentRadius ^ 2 - i ^ 2) ^ (1 / 2)
'        End If
'
'            TcircleMoveX = TcircleAimX - TcircleXP
'            TcircleMoveY = TcircleAimY - TcircleYP
'
'
'
'        If Abs(TcircleMoveX) > Abs(TcircleMoveY) Then
'            calT = Abs(TcircleMoveX) / Val(vel)
'        Else
'            calT = Abs(TcircleMoveY) / Val(vel)
'        End If
'
'
'        t = t + 0.02 + calT
'
'        TcircleXP = TcircleAimX
'        TcircleYP = TcircleAimY
'
'    Next
'
'    t = 2 * t
'
'    Timer1.Enabled = True
'
'
'    If t > 60 Then
'        flagSound = 1
'    Else
'        flagSound = 0
'    End If
'
'    For i = -1 * DrawRadius To DrawRadius Step 1
'        If Abs(i) = DrawRadius Then
'            circleAimX = i
'            circleAimY = 0
'        Else
'            circleAimX = i
'            circleAimY = (CurrentRadius ^ 2 - i ^ 2) ^ (1 / 2)
'        End If
'
'        circleMoveX = circleAimX - circleXP
'        circleMoveY = circleAimY - circleYP
'        circleMoveXS = Str(circleMoveX)
'        circleMoveYS = Str(circleMoveY)
'
'
'        If Abs(TcircleMoveX) > Abs(TcircleMoveY) Then
'            calT = Abs(TcircleMoveX) / Val(vel)
'        Else
'            calT = Abs(TcircleMoveY) / Val(vel)
'        End If
'
'
'        ll = circleMoveXS + blank + circleMoveYS + blank + run + enter
'
'        MSComm1.Output = ls
'
'        PauseTime = 0.02 + t
'        Start = Timer
'        Do While Timer < Start + PauseTime
'            DoEvents
'        Loop
'        Finish = Timer
'
'        circleXP = circleAimX
'        circleYP = circleAimY
'
'        'CircleXpic.Cls
'        'CircleXpic.ForeColor = &HFF00&
'        'CircleXpic.Print circleXP
'        'CircleYpic.Cls
'        'CircleYpic.ForeColor = &HFF00&
'        'CircleYpic.Print circleYP
'
'    Next
'
'    For i = DrawRadius To -1 * DrawRadius Step -1
'        If Abs(i) = DrawRadius Then
'            circleAimX = i
'            circleAimY = 0
'        Else
'            circleAimX = i
'            circleAimY = -1 * (CurrentRadius ^ 2 - i ^ 2) ^ (1 / 2)
'        End If
'
'        circleMoveX = circleAimX - circleXP
'        circleMoveY = circleAimY - circleYP
'        circleMoveXS = Str(circleMoveX)
'        circleMoveYS = Str(circleMoveY)
'
'        If Abs(TcircleMoveX) > Abs(TcircleMoveY) Then
'            calT = Abs(TcircleMoveX) / Val(vel)
'        Else
'            calT = Abs(TcircleMoveY) / Val(vel)
'        End If
'
'
'        ll = circleMoveXS + blank + circleMoveYS + blank + run + enter
'
'        MSComm1.Output = ls
'
'        PauseTime = 0.02 + t
'        Start = Timer
'        Do While Timer < Start + PauseTime
'            DoEvents
'        Loop
'        Finish = Timer
'
'        circleXP = circleAimX
'        circleYP = circleAimY
'
'        'CircleXpic.Cls
'        'CircleXpic.ForeColor = &HFF00&
'        'CircleXpic.Print circleXP
'        'CircleYpic.Cls
'        'CircleYpic.ForeColor = &HFF00&
'        'CircleYpic.Print circleYP
'
'    Next
'
'    If flagDisStage = 1 Then
'        circleXP = -1 * circleXP
'        circleYP = -1 * circleYP
'    End If
'
'End Sub
'
'Private Sub StartingPoint_Click()
'
'    If CurrentRadius > 0 Then
'        sent = "-5000 -5000 5000 5000 setlimit" + enter
'        Debug.Print sent
'        MSComm1.Output = sent
'
'
'        sent = "1 1 setunit" + enter ' x axis
'        Debug.Print sent
'        MSComm1.Output = sent
'
'        sent = "1 2 setunit" + enter ' y axis
'        Debug.Print sent
'        MSComm1.Output = sent
'
'        sent = "1 0 setunit" + enter ' velocity
'        Debug.Print sent
'        MSComm1.Output = sent
'
'        sent = vel + "setvel" + enter
'        Debug.Print sent
'        MSComm1.Output = sent
'
'        circleSX = circleXP + CurrentRadius \ 1
'        circleSY = circleYP
'        circleSXn = -1 * circleSX
'        circleSYn = -1 * circleSY
'
'        ScircleSX = Str(circleSX)
'        ScircleSY = Str(circleSY)
'        ScircleSXn = Str(circleSXn)
'        ScircleSYn = Str(circleSYn)
'
'        If circleSX > circleSY Then
'            t = circleSX / Val(vel)
'        Else
'            t = circleSY / Val(vel)
'        End If
'
'        If t > 1 Then
'            Timer1.Enabled = True
'        End If
'
'
'        CircleInfo.Cls
'        CircleInfo.Print "                       Processing. Please wait."
'
'        CircleXpic.Cls
'
'        CircleXpic.ForeColor = &HFF00&
'
'        CircleXpic.Print "Moving"
'
'
'        CircleYpic.Cls
'
'        CircleYpic.ForeColor = &HFF00&
'
'        CircleYpic.Print "Moving"
'
'        ls = ScircleSX + blank + ScircleSY + blank + run + enter
'        ll = ScircleSXn + blank + ScircleSYn + blank + run + enter
'
'        If flagDisStage = 0 Then
'
'            MSComm1.Output = ll
'            circleXP = -1 * CurrentRadius \ 1
'            circleYP = 0
'
'        ElseIf flagDisStage = 1 Then
'
'            MSComm1.Output = ls
'            circleXP = CurrentRadius \ 1
'            circleYP = 0
'
'        End If
'
'        PauseTime = 0.02 + t
'        Start = Timer
'        Do While Timer < Start + PauseTime
'            DoEvents
'        Loop
'        Finish = Timer
'
'        CircleInfo.Cls
'        CircleInfo.Print "                   Done. Choose an option below."
'
'        CircleXpic.Cls
'
'        CircleXpic.ForeColor = &HFF00&
'
'        CircleXpic.Print circleXP
'
'
'        CircleYpic.Cls
'
'        CircleYpic.ForeColor = &HFF00&
'
'        CircleYpic.Print circleYP
'    End If
'
'End Sub


'Private Sub Circle1_Click()
'
'    Menu.Visible = False
'    CircleF.Visible = True
'    CircleF.Top = 240
'    CircleF.Left = 120
'    If flagCircleFirst = 1 Then
'        flagCircleFirst = 0
'        circleXP = 0
'        circleYP = 0
'        tempRadius = Round((circleXP ^ 2 + circleYP ^ 2) ^ (1 / 2), 2)
'        radius.Text = Str(tempRadius)
'        CurrentRadius = 0
'    End If
'
'
'    CircleXpic.Cls
'
'    CircleXpic.ForeColor = &HFF00&
'
'    CircleXpic.Print circleXP
'
'
'    CircleYpic.Cls
'
'    CircleYpic.ForeColor = &HFF00&
'
'    CircleYpic.Print circleYP
'
'    radiuspic.Cls
'    radiuspic.Print CurrentRadius
'
'
'End Sub
'
'Private Sub CircleBack_Click()
'
'    Menu.Visible = True
'    CircleF.Visible = False
'
'End Sub

'Private Sub cmd_Openport_Click()

'MSComm1.PortOpen = True

'End Sub

'
'Private Sub ToyBox_Click()
'
'    If flagToyBox = 0 Then
'        arrow_frame.Left = 1320
'        arrow_frame.Top = 4560
'        ToyF.Height = 2775
'        ToyF.Width = 6615
'        flagToyBox = 1
'        Menu.Visible = True
'    ElseIf flagToyBox = 1 Then
'        arrow_frame.Left = 1320
'        arrow_frame.Top = 2600
'        ToyF.Height = 375
'        ToyF.Width = 1095
'        flagToyBox = 0
'        Menu.Visible = False
'        CircleF.Visible = False
'    End If
'    arrowXpic.Cls
'
'    arrowXpic.ForeColor = &HFF00&
'
'    arrowXpic.Print positionX
'
'
'    arrowYpic.Cls
'
'    arrowYpic.ForeColor = &HFF00&
'
'    arrowYpic.Print positionY
'
'    CircleXpic.Cls
'
'    CircleXpic.ForeColor = &HFF00&
'
'    CircleXpic.Print circleXP
'
'
'    CircleYpic.Cls
'
'    CircleYpic.ForeColor = &HFF00&
'
'    CircleYpic.Print circleYP
'
'
'End Sub

Private Sub ypic_Click()

    Advance_Pass.Visible = True
    Advance_Pass.Height = 1395
    Advance_Pass.Left = 2400
    Advance_Pass.Top = 4140
    Advance_Pass.Width = 2715

End Sub


Private Sub Command11_Click()
Dim hDCtmp As Long, picWidth As Double, picHeight As Double
Dim X As Double
Dim Y As Double
Dim pixel As Double


X = Val(Text11.Text)
Y = Val(Text12.Text)
picWidth = Val(100)
picHeight = Val(100)
hDCtmp = GetDC(0)
Picture1.AutoRedraw = True
BitBlt Picture1.hdc, 0, 0, picWidth, picHeight, hDCtmp, X, Y, vbSrcCopy
ReleaseDC 0, hDCtmp

'StageControl.ScaleMode = 3
Picture1.ScaleMode = 3
'Picture1.ScaleHeight = 200
'Picture1.ScaleWidth = 200

Dim picPixel(101, 101) As Integer
Dim i, j As Integer
Dim r, g, b As Double
Dim count As Double
Dim count2, count3 As Double
Dim max, min As Integer
Dim limit, limit2 As Double
limit = Val(Text18.Text)
limit2 = Val(Text19.Text)
count = 0   'total
count2 = 0  'green
count3 = 0
max = 0
min = 255

For i = 1 To 100
    For j = 1 To 100
        pixel = Picture1.Point(i, j)
        r = pixel Mod 256
        g = (pixel \ 256) Mod 256
        b = pixel \ 256 \ 256
        picPixel(i, j) = (r + g + b) / 3
        If picPixel(i, j) > max Then
            If picPixel(i, j) = 240 Then
            
            Else
                max = picPixel(i, j)
            End If
        End If
        If picPixel(i, j) < min Then
            If picPixel(i, j) = 240 Then
            
            Else
                min = picPixel(i, j)
            End If
        End If
        If g > Val(Text13.Text) Then
            count = count + 1
        End If
        If g > limit * r Then
            If g > limit * b Then
                count2 = count2 + 1
            End If
        End If
        If Abs(g - r) < (limit2 * g) Then
            If Abs(g - b) < (limit2 * g) Then
                count3 = count3 + 1
            End If
        End If
        
    Next
Next


'For i = 1 To 100
'    For j = 1 To 100
'        If picPixel(i, j) > max Then
'            max = picPixel(i, j)
'            Text15.Text = j
'        End If
'        If picPixel(i, j) < min Then
'            min = picPixel(i, j)
'        End If
'        If picPixel(i, j) > Text13.Text Then
'            count = count + 1
'        End If
'    Next
'Next

Text7.Text = max
Text8.Text = min
Text16.Text = count2
Text17.Text = count3
Text10.Text = count

'For i = 1 To 100
'    For j = 1 To 100
'        If picPixel(i, j) < 100 Then
'            count = count + 1
'        End If
'    Next
'Next

'Dim picPixel(101, 101, 4) As Integer
'Dim i, j As Integer
'Dim r, g, b As Integer
'Dim count As Double
'
'count = 0
'Picture1.PSet (100, 100), vbRed
'
'For i = 1 To 100
'    For j = 1 To 100
'        pixel = Picture1.Point(i, j)
'        picPixel(i, j, 1) = pixel Mod 256
'        picPixel(i, j, 2) = (pixel \ 256) Mod 256
'        picPixel(i, j, 3) = pixel \ 256 \ 256
'        picPixel(i, j, 4) = (picPixel(i, j, 1) + picPixel(i, j, 2) + picPixel(i, j, 3)) / 3
'    Next
'Next
'
'
'
'Text7.Text = picPixel(50, 50, 1)
'Text8.Text = picPixel(50, 50, 2)
'Text10.Text = picPixel(50, 50, 3)
'Text8.Text = picPixel(50, 50)
'Text7.Text = picPixel(30, 30)
'Picture1.Picture = Picture1.Image
'SavePicture Picture1.Image, App.Path & "\image\temp.bmp"

'Text7.Text = Picture1.Width

End Sub



Public Sub calDrawRegion()

    Dim picDrawX As Integer
    Dim picDrawY As Integer
    Dim startValue As Integer
    Dim endValue As Integer
    Dim sameRegion As Boolean

    Dim haveColorPre As Boolean
    Dim haveColorNow As Boolean
    Dim iniP As Boolean
    Dim Xpic, ypic As String
    Dim flagExtra As Boolean
    Dim countCorrect As Integer
    Dim StepSizeX As Double
    Dim progressNum As Integer
    Dim progressDivide As Double
    progressNum = 1
    progressDivide = picWidth / 34
    StepSizeX = DrawPicStepX.Text
    'Dim flagCorrect As bollean
    

    picDrawCorrect = 100000
    countCorrect = 0
    testCorrection = 2
    'flagCorrect = False

    flagExtra = False


    
    If newPixelPannel(DrawPicStartValue, 1) < picRegionMax Then
        If newPixelPannel(DrawPicStartValue, 1) > picRegionMin Then
            haveColorPre = True
        End If
'       ElseIf newpixelpannel(1, 1) > picRegionWhite Then
        Else
            haveColorPre = False
        End If
    
    If shutterIsOpen = True Then
        shutterClose
    End If
    

    DrawPicProgress.Cls
    DrawPicProgress.FontSize = 12
    
    
    For picDrawX = 1 To picWidth
    
    
            If picDrawX Mod 2 = 1 Then
            
            ypic = Str(testCorrection * -1)
            Xpic = Str(0)
            lpic = Xpic + blank + ypic + blank + run + enter
            'MSComm1.Output = lpic
            DrawPicTime1 = DrawPicTime1 + (Abs(Val(Xpic) / Val(vel)) * 10000 + 1000)
            
                For picDrawY = 1 To picHeight
                    
                    haveColorNow = False
                    If newPixelPannel(picDrawX, picDrawY) < picRegionMax Then
                        If newPixelPannel(picDrawX, picDrawY) > picRegionMin Then
                            haveColorNow = True
                        Else
                            haveColorNow = False
                        End If
    '                ElseIf newpixelpannel(picDrawX, picDrawY) > picRegionWhite Then
                    Else
                        haveColorNow = False
                    End If
                    
                    If haveColorNow = haveColorPre Then
                        sameRegion = True
                    Else
                        sameRegion = False
                    End If
                    
    
                    If picDrawY = 1 Then
                        startValue = 1
                    End If
                    
                    If picDrawY < picHeight Then
                    
                        If sameRegion = False Then
                            drawLength = picDrawY - startValue
                            
                            If haveColorPre = True Then
                            
                                drawLength = drawLength - 1
    '                            If startValue = 1 Then
    '                                drawLength = drawLength + 1
    '                            End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
    
                                If drawLength > 0 Then
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                    ypic = Str(-1 * drawLength)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    'MSComm1.Output = lpic
                                    'countnum
                                    CorYV.Text = CorYV.Text - drawLength
                                    Text1.Text = "y-" & drawLength
                                    DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                    
                                    countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
                                ElseIf drawLength = 0 Then
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                
                            ElseIf haveColorPre = False Then
                                
                                If startValue = 1 Then
                                    drawLength = drawLength
                                Else
                                    drawLength = drawLength + 1
                                End If
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                ypic = Str(-1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                'MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text - drawLength
                                Text1.Text = "y-" & drawLength
                                DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                            End If
                                
                            startValue = picDrawY
                                
                        End If
                    
                    
                    ElseIf picDrawY = picHeight Then
                        If sameRegion = True Then
                            If haveColorNow = True Then
                            
                                drawLength = picHeight - startValue
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If drawLength > 0 Then
                                   DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                   ypic = Str(-1 * drawLength)
                                   Xpic = Str(0)
                                   lpic = Xpic + blank + ypic + blank + run + enter
                                   'MSComm1.Output = lpic
                                   'countnum
                                   CorYV.Text = CorYV.Text - drawLength
                                   Text1.Text = "y-" & drawLength
                                   DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                   DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                   
                                   countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                                ElseIf drawLength = 0 Then
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                            
                            ElseIf haveColorNow = False Then
                            
                                drawLength = picHeight + 1 - startValue
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                ypic = Str(-1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                'MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text - drawLength
                                Text1.Text = "y-" & drawLength
                                DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                            
                            End If
                        
 
                        
                        End If
                        
    
    
            
                    
                        
                        If shutterIsOpen = True Then
                            shutterClose
                        End If
                        ypic = Str(0)
                        Xpic = Str(StepSizeX)
                        
                        lpic = Xpic + blank + ypic + blank + run + enter
                        'MSComm1.Output = lpic
                        CorXV.Text = CorXV.Text + 1
                        Text14.Text = Text14.Text + 1
                        DrawPicTime1 = DrawPicTime1 + (2 * StepSizeX / Val(vel) * 10000 + 200)
                        
                        If picDrawX < picWidth Then
                        
                            If newPixelPannel(picDrawX + 1, picHeight) < picRegionMax Then
                                If newPixelPannel(picDrawX + 1, picHeight) > picRegionMin Then
                                    haveColorNow = True
                                End If
                            
    '                        ElseIf newpixelpannel(picDrawX + 1, picHeight) > picRegionMin Then
                            Else
                                haveColorNow = False
                            End If
                            
                        End If
                        
                    End If
                    
                    haveColorPre = haveColorNow
          
                Next
                
            ElseIf picDrawX Mod 2 = 0 Then
            
            ypic = Str(testCorrection)
            Xpic = Str(0)
            lpic = Xpic + blank + ypic + blank + run + enter
            'MSComm1.Output = lpic
            DrawPicTime1 = DrawPicTime1 + (Abs(Val(Xpic) / Val(vel)) * 10000 + 100)
            
                For picDrawY = picHeight To 1 Step -1
                    haveColorNow = False
                    If newPixelPannel(picDrawX, picDrawY) < picRegionMax Then
                        If newPixelPannel(picDrawX, picDrawY) > picRegionMin Then
                            haveColorNow = True
                        Else
                            haveColorNow = False
                        End If
    '                ElseIf newpixelpannel(picDrawX, picDrawY) > picRegionMin Then
                    Else
                        haveColorNow = False
                    End If
                    
                    If haveColorNow = haveColorPre Then
                        sameRegion = True
                    Else
                        sameRegion = False
                    End If
                    
    
                    If picDrawY = picHeight Then
                        startValue = picHeight
                    End If
                    
                    If picDrawY > 1 Then
                    
                        If sameRegion = False Then
                            drawLength = startValue - picDrawY
                            
                            If haveColorPre = True Then
                            
                                drawLength = drawLength - 1
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If drawLength > 0 Then
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                    ypic = Str(1 * drawLength)
                                    Xpic = Str(0)
                                    lpic = Xpic + blank + ypic + blank + run + enter
                                    'MSComm1.Output = lpic
                                    'countnum
                                    CorYV.Text = CorYV.Text + drawLength
                                    Text1.Text = "y" & drawLength
                                    DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                    
                                    countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                                ElseIf drawLength = 0 Then
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                
                            ElseIf haveColorPre = False Then
                                    
                                If startValue = picHeight Then
                                    drawLength = drawLength
                                Else
                                    drawLength = drawLength + 1
                                End If
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                ypic = Str(1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                'MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text + drawLength
                                Text1.Text = "y" & drawLength
                                DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                            End If
                            startValue = picDrawY
                        End If
                    
                    
                    ElseIf picDrawY = 1 Then
                        If sameRegion = True Then
                            If haveColorNow = True Then
                            
                                drawLength = startValue - 1
                                If shutterIsOpen = False Then
                                    shutterOpen
                                End If
                                If drawLength = 1 Then
                                    drawLength = 1
                                    'flagExtra = True
                                End If
                                If drawLength > 0 Then
                                   DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                   ypic = Str(1 * drawLength)
                                   Xpic = Str(0)
                                   lpic = Xpic + blank + ypic + blank + run + enter
                                   'MSComm1.Output = lpic
                                   'countnum
                                   CorYV.Text = CorYV.Text + drawLength
                                   Text1.Text = "y" & drawLength
                                   DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                   DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                   
                                   countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
                                ElseIf drawLength = 0 Then
                                    DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000 + 200)
                                End If
                                
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                            
                            ElseIf haveColorNow = False Then
    
                                drawLength = startValue - 1 + 1
                                If shutterIsOpen = True Then
                                    shutterClose
                                End If
                                If flagExtra = True Then
                                    drawLength = drawLength + 1
                                    flagExtra = False
                                End If
                                ypic = Str(1 * drawLength)
                                Xpic = Str(0)
                                lpic = Xpic + blank + ypic + blank + run + enter
                                'MSComm1.Output = lpic
                                'countnum
                                CorYV.Text = CorYV.Text + drawLength
                                Text1.Text = "y" & drawLength
                                DrawPicTime1 = DrawPicTime1 + (drawLength / Val(vel) * 10000 + 200)
                                
                                countCorrect = countCorrect + 1
                                    If countCorrect > picDrawCorrect Then
                                        ypic = Str(-1)
                                        Xpic = Str(0)
                                        lpic = Xpic + blank + ypic + blank + run + enter
                                        'MSComm1.Output = lpic
                                        DrawPicTime1 = DrawPicTime1 + (1 / Val(vel) * 10000)
                                        countCorrect = 1
                                    End If
    
    
                            End If
    '

                        
                        End If
                        
    
                        
    
                        
                        If shutterIsOpen = True Then
                            shutterClose
                        End If
                        ypic = Str(0)
                        Xpic = Str(StepSizeX)
                        
                        lpic = Xpic + blank + ypic + blank + run + enter
                        'MSComm1.Output = lpic
                        CorXV.Text = CorXV.Text + 1
                        Text14.Text = Text14.Text + 1
                        DrawPicTime1 = DrawPicTime1 + (2 * StepSizeX / Val(vel) * 10000 + 200)
                        
                        If picDrawX < picWidth Then
                        
                            If newPixelPannel(picDrawX + 1, 1) < picRegionMax Then
                                If newPixelPannel(picDrawX + 1, 1) > picRegionMin Then
                                    haveColorNow = True
                                End If
    '                        ElseIf newpixelpannel(picDrawX + 1, 1) > picRegionMin Then
                            Else
                                haveColorNow = False
                            End If
                            
                        End If
                        
                    End If
                    
                    haveColorPre = haveColorNow
          
                Next
            End If
            
        If picDrawX / progressDivide > progressNum Then
            progressNum = progressNum + 1
            DrawPicProgress.Print "l";
        End If

    Next
    DrawPicProgress.Cls
    
End Sub

'Private Sub Command12_Click()
'
'    Dim temp As Integer
'    Input #2, temp
'    Text23.Text = temp
'
'End Sub

Private Sub SaveVariable_Click()
    
    SaveData

End Sub

Private Sub inputData()

    Dim temp As Integer
    Open (App.Path & "\save\data.inf") For Input As #2
    Input #2, temp
    DrawPicMin.Text = temp
    Input #2, temp
    DrawPicMax.Text = temp
    Close #2

End Sub

Private Sub SaveData()
    Open (App.Path & "\save\data.inf") For Output As #3
    Write #3, Val(DrawPicMin.Text)
    Write #3, Val(DrawPicMax.Text)
    Close #3
End Sub
