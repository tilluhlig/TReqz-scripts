import argparse

if __name__ == "__main__":

    def runReqifToLatex(args):
        print("<<< convert reqif to latex >>>")
        import convertReqifToLatex
        convertReqifToLatex.convertReqifToLatex(args.input, args.output, args.width, args.images)
        print("done")

    def runReqifToExcel(args):
        print("<<< convert reqif to excel >>>")
        raise NotImplementedError

    def runExcelToReqif(args):
        print("<<< convert excel to reqif >>>")
        raise NotImplementedError

    main_parser = argparse.ArgumentParser(conflict_handler='resolve')
    subparsers = main_parser.add_subparsers()

    # reqif_to_latex
    reqif_to_latex_parser = subparsers.add_parser('reqif_to_latex', help='???')
    reqif_to_latex_parser.add_argument('--input', help='???', required=True, type=str)
    reqif_to_latex_parser.add_argument('--output', help='???', type=str, default="output.tex")
    reqif_to_latex_parser.add_argument('--width', help='???', type=str, default="15cm")
    reqif_to_latex_parser.add_argument('--images', help='???', action='store_true')
    reqif_to_latex_parser.set_defaults(func=runReqifToLatex)

    # reqif_to_excel
    reqif_to_excel_parser = subparsers.add_parser('reqif_to_excel', help='???')
    reqif_to_excel_parser.add_argument('--input', help='???', required=True, type=str)
    reqif_to_excel_parser.add_argument('--output', help='???', type=str, default="output.xsl")
    reqif_to_excel_parser.set_defaults(func=runReqifToExcel)

    # excel_to_reqif
    excel_to_reqif_parser = subparsers.add_parser('excel_to_reqif', help='???')
    excel_to_reqif_parser.add_argument('--input', help='???', required=True, type=str)
    excel_to_reqif_parser.add_argument('--output', help='???', type=str, default="output.reqif")
    excel_to_reqif_parser.set_defaults(func=runExcelToReqif)

    #args = ['reqif_to_latex', '--input=input.reqif']
    args = main_parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)  # call the default function
    else:
        main_parser.print_help()