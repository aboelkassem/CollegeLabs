/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.solutions;

/**
 *
 * @author Mohamed
 */
public class Service {
    private int SERVICE_ID;
    private String NAME;
    private String DESCRIPTION;
    private String OFFER;
    private String PLATFORM;
    private int COURSE_ID;

    public Service(int SERVICE_ID, String NAME, String DESCRIPTION, String OFFER, String PLATFORM, int COURSE_ID) {
        this.SERVICE_ID = SERVICE_ID;
        this.NAME = NAME;
        this.DESCRIPTION = DESCRIPTION;
        this.OFFER = OFFER;
        this.PLATFORM = PLATFORM;
        this.COURSE_ID = COURSE_ID;
    }

    public int getCOURSE_ID() {
        return COURSE_ID;
    }

    public String getDESCRIPTION() {
        return DESCRIPTION;
    }

    public String getNAME() {
        return NAME;
    }

    public String getOFFER() {
        return OFFER;
    }

    public String getPLATFORM() {
        return PLATFORM;
    }

    public int getSERVICE_ID() {
        return SERVICE_ID;
    }
    
    
}
