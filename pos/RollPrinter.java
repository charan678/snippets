package jade.printer;

import jade.model.JadeProduct;

import java.awt.Canvas;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.font.FontRenderContext;
import java.awt.font.TextLayout;
import java.awt.print.PageFormat;
import java.awt.print.Paper;
import java.awt.print.Printable;
import java.awt.print.PrinterException;
import java.awt.print.PrinterJob;
import java.util.ArrayList;
import java.util.Set;

import javax.print.attribute.standard.Severity;
import javax.print.PrintService;
import javax.print.attribute.HashPrintRequestAttributeSet;
import javax.print.attribute.PrintRequestAttributeSet;
import javax.print.attribute.standard.Copies;
import javax.print.attribute.standard.PrinterStateReason;
import javax.print.attribute.standard.PrinterStateReasons;
 

public class RollPrinter implements Printable {

    int[] pageBreaks;
    ArrayList<TextLayout> textLines;
    FontMetrics metrics = null;
    FontRenderContext currentFrc = null;
    int pageIndex = 0;
    int lineHeight = 0;
    int currentHeight = 0;
    int staticWidth = 10;
    PageFormat pfmt = null;
    Paper paper = null;
    //Maximum character for Item line
    int maxItemLength = 10;
    java.util.List<JadeProduct> rowItems = null;//new ArrayList<ItemModel>();
    Font currentFont = null;
    
    String billNo = "";
    String cardNo ="";
    String pytType="";
    String dateTrans = "";
    String cardBalance = "";
    String total = "";
    String terminal = "";
    String printerName = "Bullzip PDF Printer";
    
    
    public RollPrinter(java.util.List<JadeProduct> rowItems,String billNo,String cardNo, String pytType, String dateTrans, String total, String cardBalance, String terminal){
    	this(rowItems,billNo,cardNo,pytType,dateTrans,total, cardBalance);
    	this.terminal = terminal;
    } 
    public RollPrinter(java.util.List<JadeProduct> rowItems,String billNo,String cardNo, String pytType, String dateTrans, String total, String cardBalance){        
        
    	this.rowItems = rowItems;
    	this.billNo = billNo;
        this.cardNo = cardNo;
        this.pytType = pytType;
        this.dateTrans = dateTrans;
        this.total = total;
        this.cardBalance = cardBalance;
    	currentFont = new Font("Courier", Font.BOLD, 10);
    	
    	paper = new Paper();
        double dotsperinch = 72;
        double margin = 0.125*dotsperinch;
        double w = 8.5*dotsperinch;        
        double h = paper.getHeight() + heightPage();
        paper.setImageableArea(margin, margin, w-2*margin, h-2*margin);
        paper.setSize(w, h);
        pfmt = new PageFormat();
        pfmt.setPaper(paper);    
        System.out.println("bill no ="+billNo + ", pytType ="+pytType +", cardNo="+cardNo);
    }
    
    
    public int heightPage(){
    	
    	Canvas c = new Canvas();
        FontMetrics metrics2 = c.getFontMetrics(this.currentFont);
        int heightLined =  metrics2.getHeight();
        int headerHeight = 8 * heightLined;
        int bodyHeight = 2 * heightLined + rowItems.size() * heightLined + 2 * heightLined;
        int footerHeight = 3 * heightLined;
        return headerHeight + bodyHeight + footerHeight;
    }


    
    
    public void setStyle(Graphics g, Font font){
        currentFont = font;
        FontMetrics metrics = g.getFontMetrics(currentFont);
        this.lineHeight = metrics.getHeight();
        g.setFont(currentFont);
        Graphics2D g2d = (Graphics2D)g;
        currentFrc = g2d.getFontRenderContext();
    }

    public void updateHeight(){
        currentHeight += this.lineHeight;
    }

    public void updateHeight(int height){
        currentHeight += height;   
    }


    public void header(Graphics g, PageFormat pf) throws Exception{
        try{
            
            TextLayout header = new TextLayout("Jade Payments: Sales Receipt",currentFont,currentFrc);
            header.draw((Graphics2D)g,staticWidth, currentHeight);
            updateHeight();
            
            g.drawLine(0,currentHeight,200,currentHeight);
            updateHeight();
            
            header = new TextLayout("Card No: "+this.cardNo,currentFont,currentFrc);
            header.draw((Graphics2D)g,staticWidth, currentHeight);
            updateHeight();

            header = new TextLayout("Bill No: "+this.billNo,currentFont,currentFrc);
            header.draw((Graphics2D)g,staticWidth, currentHeight);
            updateHeight();
            
            header = new TextLayout("Terminal id: "+this.terminal,currentFont,currentFrc);
            header.draw((Graphics2D)g,staticWidth, currentHeight);
            updateHeight();
            
            header = new TextLayout("Pyt Type: "+this.pytType,currentFont,currentFrc);
            header.draw((Graphics2D)g,staticWidth, currentHeight);
            updateHeight();

            header = new TextLayout("Date: "+this.dateTrans,currentFont,currentFrc);
            header.draw((Graphics2D)g,staticWidth, currentHeight);
            updateHeight();
            
            g.drawLine(0,currentHeight,200,currentHeight);
            updateHeight();
        
        }
        catch(Exception e){
            System.out.println(e);
            e.printStackTrace();
        }
    }

     
    public void bodyStructure(Graphics g){
    TextLayout  tempLayout = null;
    // Header  
 	tempLayout = new TextLayout("Item", currentFont , currentFrc);
 	tempLayout.draw((Graphics2D)g, staticWidth, currentHeight);
 	tempLayout = new TextLayout("Qty",currentFont ,currentFrc);
 	tempLayout.draw((Graphics2D)g,90,currentHeight);
 	tempLayout = new TextLayout("Price", currentFont , currentFrc);
 	tempLayout.draw((Graphics2D)g,150,currentHeight);        
 	updateHeight();
 	
 	//Line
	g.drawLine(0,currentHeight,200,currentHeight);
	updateHeight();
    
    
    for(int i=0;i < this.rowItems.size() ;i++){
        ArrayList<String> temp = null;
        temp = new ArrayList<String>();
        String tempStr = "";
        JadeProduct itemObj = rowItems.get(i);    
        if( itemObj.getItem().length() >= maxItemLength){
        	int tempNum = itemObj.getItem().length()/(maxItemLength+1);    
            for(int k=0; k<=tempNum; k++){
            	if(k==0){
            		tempStr = itemObj.getItem().substring(0,maxItemLength-1);
                }
                else{
                    if(itemObj.getItem().length() >= ((k+1)*maxItemLength)-1){
                    	temp.add(itemObj.getItem().substring(k*maxItemLength-1,((k+1)*maxItemLength) -1 )); 
                     }
                     else{
                    	 temp.add(itemObj.getItem().substring(k*maxItemLength,itemObj.getItem().length()));
                      	 }
                    }
            }
        }
        else{
           tempStr = itemObj.getItem();
        }
        
        if(temp==null){
            tempLayout = new TextLayout(tempStr, currentFont , currentFrc);
            tempLayout.draw((Graphics2D)g, staticWidth, currentHeight);
            tempLayout = new TextLayout(""+itemObj.getQty(),currentFont ,currentFrc);
            tempLayout.draw((Graphics2D)g,90,currentHeight);
            tempLayout = new TextLayout(""+itemObj.getPrice(), currentFont , currentFrc);
            tempLayout.draw((Graphics2D)g,150,currentHeight);        
            updateHeight();
        }
        else{
                tempLayout = new TextLayout(tempStr, currentFont , currentFrc);
                tempLayout.draw((Graphics2D)g, staticWidth, currentHeight);
                tempLayout = new TextLayout(""+itemObj.getQty(),currentFont ,currentFrc);
                tempLayout.draw((Graphics2D)g,90,currentHeight);
                tempLayout = new TextLayout(""+itemObj.getPrice(), currentFont , currentFrc);
                tempLayout.draw((Graphics2D)g,150,currentHeight);        
                updateHeight();
                System.out.println("temp ="+temp);
                for(int l=0;l<temp.size();l++){
                    tempLayout = new TextLayout(temp.get(l), currentFont , currentFrc);
                    tempLayout.draw((Graphics2D)g,staticWidth,currentHeight);
                    updateHeight();
                }
        }
        
        
    }
        
	//Line
	g.drawLine(0,currentHeight,200,currentHeight);
	updateHeight();
	// For total 
	tempLayout = new TextLayout("Total", currentFont , currentFrc);
	tempLayout.draw((Graphics2D)g, staticWidth, currentHeight);
	tempLayout = new TextLayout("-",currentFont ,currentFrc);
	tempLayout.draw((Graphics2D)g,70,currentHeight);
	tempLayout = new TextLayout(""+total, currentFont , currentFrc);
	tempLayout.draw((Graphics2D)g,150,currentHeight);        
	updateHeight();
	
	//Card balance
	tempLayout = new TextLayout("Card Bal", currentFont , currentFrc);
	tempLayout.draw((Graphics2D)g, staticWidth, currentHeight);
	tempLayout = new TextLayout("-",currentFont ,currentFrc);
	tempLayout.draw((Graphics2D)g,70,currentHeight);
	tempLayout = new TextLayout(this.cardBalance, currentFont , currentFrc);
	tempLayout.draw((Graphics2D)g,150,currentHeight);        
	updateHeight();
	
	//Line 
	g.drawLine(0,currentHeight,200,currentHeight);
	updateHeight();

    //}   
    
    
    
    }


    public void body(Graphics g, PageFormat pf){
        Graphics2D g2d = (Graphics2D)g;
        //Set up the Body Structure
        bodyStructure(g);
    }


    public void footer(Graphics g,PageFormat pf) {
        TextLayout  text1 = new TextLayout("Thanks For Shopping.", currentFont , currentFrc);
        text1.draw((Graphics2D)g,staticWidth, currentHeight);
        updateHeight();

        
    }

    @Override
    public int print(Graphics g, PageFormat pf, int pageIndex) throws PrinterException {
        try{
         
            setStyle(g, currentFont);
            if(pageIndex  > 0){ 
                return NO_SUCH_PAGE;  
            }
            if(pageIndex ==0){
                    this.header(g,pf);
            }
            this.body(g,pf);
            this.footer(g,pf);
        }
        catch(Exception e){
            e.printStackTrace();
        }
        return PAGE_EXISTS;
    }

    
    
public String getPrinter(){
	return this.printerName;
}

public String[] listPrinters(){
	
	String[] printerList = null;
	int count = 0;
    
	PrinterJob job = PrinterJob.getPrinterJob();
    PrintService[] service = PrinterJob.lookupPrintServices();
    count = service.length;
    
    if(count != 0){
	    printerList = new String[count]; 
	    for (int i = 0; i < count; i++) {
	    printerList[i] = service[i].getName();   	
	    }
    }
    return printerList;
}

public void setPrinter(String printerName){
	
	this.printerName = printerName;
} 
    
    
  // This is will call print function
  public void printOut() throws PrinterException{
        
        PrinterJob job = PrinterJob.getPrinterJob();
        job.setPrintable(this,this.pfmt);
        
        PrintRequestAttributeSet attr_set = new HashPrintRequestAttributeSet();
        
        attr_set.add(new Copies(1)); 
        
        //PrintService[] service = PrinterJob.lookupPrintServices();
        //int count = service.length;
        //DocPrintJob docPrintJob = null;
        /*
        for (int i = 0; i < count; i++) {
            if (service[i].getName().equalsIgnoreCase(printerName)) {
                docPrintJob = service[i].createPrintJob();
                i = count;
            }
        }
		*/
        
        if(job !=null){
            try {
            	String returnReason = "";
            	PrinterStateReasons psr = job.getPrintService().getAttribute(PrinterStateReasons.class);
                if (psr != null) {
                  Set<PrinterStateReason> errors = psr.printerStateReasonSet(Severity.REPORT);
                  for (PrinterStateReason reason : errors)
                	  returnReason += reason.getName();  
                  throw new PrinterException("Alert : %s"+returnReason);
                }          
                job.print();
                
			} catch (PrinterException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
				throw e;
			}
        }
        else{
                try {
		        	throw new PrinterException("No Printer Service available = "+printerName);        	
				} catch (PrinterException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					throw e;
				}
        }

         
  }


}
